# coding=utf-8

import json
import logging
import re

from vp_manager.operation.advanced import vp as plugin_control, \
    account as account_control, copy_chat as copy_control
from vp_manager.config import account as account_config, const
from vp_manager.utils.exceptions import VPException
from vp_manager.data.missions import mission_list as global_mission_list
from vp_manager.data.followers import follower_list as global_follower_list
from vp_manager.data.rewards import reward_list
from vp_manager.engine.database import get_win_arranges, update_arrangement

logger = logging.getLogger(__name__)

message_patterns = {
    const.MT_ROLE_DATA: re.compile(r'##ROLE_DATA##(.*?)##'),
    const.MT_MISSION_DATA: re.compile(r'##MT_MISSION_DATA##(.*?)##'),
    const.MT_MISSION_RESULT: re.compile(r'##MISSION_RESULT##(.*?)##'),
    const.MT_FOLLOWER_INFO: re.compile(r'##MISSION_RESULT##(.*?)##'),
    const.MT_SOLDIER_LEVEL: re.compile(r'##MISSION_RESULT##(\d+)##'),
}


class Engine:

    def __init__(self):  # TODO: muti window
        self.current_role = account_config.efficient_role[0]  # role name
        self.role_data = {}  # role name, anima
        self.follower_data = {}  # follower_level, soldier level
        self.mission_list = []  # just record first 6 missions, mission id, name, type, time, cost, level, reward

    def start(self):
        while True:
            try:
                account_control.open_client()
                self.work()
            except VPException as e:
                logger.error(e.msg)
            account_control.close_client()

    def get_message(self, clear=True):
        copy_control.open_window()
        text = copy_control.copy_text()
        copy_control.close_window(clear)

        return text

    def work(self):
        role = self.current_role

        while True:
            self.login(role)
            anima = self.role_data['anima']
            if int(anima) < 100:
                logger.warning(f'{self.current_role} anima is {anima}, will skip this role')
            else:
                logger.info(f'{self.current_role} anima is {anima}, start manage missions')
                self.manage_missions()

            role = self.get_next_role(self.current_role, account_config.efficient_role)
            logger.info(f'{self.current_role} end manage missions, will switch to {role}')
            account_control.logout()
            self.role_data = {}

    def login(self, role):
        account_control.choose_role(role, self.current_role, account_config.total_role)
        account_control.enter_game()
        account_control.print_role_info()

        text = self.get_message()
        pattern = message_patterns.get(const.MT_ROLE_DATA)
        self.role_data = json.loads(pattern.findall(text)[-1])
        self.current_role = self.role_data['name']
        logger.info(f'login role {self.current_role}')

    def manage_missions(self):

        plugin_control.open_venture_plan()
        plugin_control.complete_missions()

        index = 0

        while index < 6:  # only do first 6 missions
            status = self.execute_mission(index)
            if status == const.MER_FAILED:
                index += 1
            elif status == const.MER_END:
                break

        plugin_control.start_all_missions()

    def execute_mission(self, index):
        """
        mission: {
            "id": 123,
            "level": 48,
            "reward": {
                "id": "1234 1235",
                "type": "gold"
            }
        }

        follower_data: [
            {
                "id": 123,
                "level": 47,
                "health": 1230
            },
            ...
        ]
        soldier_level: 47


        :param index:
        :return:
        """

        # 1. click button into mission view
        plugin_control.enter_mission_view(index)

        # 2. print and get follower_data, mission_data
        text = self.get_message()
        m_pattern = message_patterns.get(const.MT_MISSION_DATA)
        f_pattern = message_patterns.get(const.MT_FOLLOWER_INFO)
        s_pattern = message_patterns.get(const.MT_SOLDIER_LEVEL)

        mission = json.loads(m_pattern.findall(text)[-1])  # id, level
        followers = json.loads(f_pattern.findall(text)[-1])[:4]  # only search first 4 followers
        s_level = json.loads(s_pattern.findall(text)[-1])

        if not (mission and followers and s_level):
            logger.warning(f'can not get mission data, will end scan.')
            return const.MER_END

        if not self.is_mission_end(mission):
            logger.info(f'got trash mission, will end scan. {mission["id"]} {mission["name"]}')
            return const.MER_END

        if not self.is_mission_worth(mission):
            logger.info(f'got worthless mission, will skip it. {mission["id"]} {mission["name"]} {mission["reward"]["type"]}')
            return const.MER_FAILED

        m_id, m_level = mission['id'], mission['level']
        mission = self.add_mission_field(mission)
        if not mission:
            logger.warning(f"Unknown mission id: {m_id}")
            return const.MER_FAILED

        follower = self.get_arrangement_by_storage(mission, s_level, followers)

        is_mission_win = False
        if not follower:
            pass
        elif follower['status'] == const.FFR_MUST_WIN:
            is_mission_win = True
            logger.info(f'get arrangement by cache success, will arrange ({follower["level"]}) {follower["name"]} '
                        f'({follower["health"]}) for mission ({m_level}){mission["name"]}, arrangement is {follower["arrangement"]}')
            plugin_control.assign_follower_team(follower['arrangement'], follower['index'])
        elif follower['status'] == const.FFR_NOT_SURE or follower['status'] == const.FFR_UNKNOWN:
            arrange = self.get_arrangement_by_plugin(follower)
            follower['arrangement'] = arrange
            # TODO: update in new thread
            update_arrangement(mission=mission, follower=follower, s_level=s_level)
            if arrange:
                is_mission_win = True
                logger.info(f'get arrangement by plugin success, will arrange ({follower["level"]}) {follower["name"]} '
                            f'({follower["health"]}) for mission ({m_level}){mission["name"]}, arrangement is {arrange}')

        if is_mission_win:
            plugin_control.confirm_mission()
            self.role_data['anima'] = self.role_data['anima'] - mission['cost'] - 4
            return const.MER_SUCCESS
        else:
            plugin_control.close_mission_view()
            logger.info(f'mission ({m_level}){mission["name"]} will fail anyway')
            return const.MER_FAILED

    def get_arrangement_by_storage(self, mission, s_level, followers):
        """
            followers: the first 4 followers
        """

        result = get_win_arranges(mission=mission, s_level=s_level, followers=followers)
        result = {item['f_id']: item for item in result}

        final_follower = None

        for i, follower in enumerate(followers):
            follower['index'] = i  # position
            follower['name'] = global_follower_list[follower['id']]
            f_id, f_health = follower['id'], follower['health']
            record = result.get(f_id)
            if not record:
                follower['status'] = const.FFR_UNKNOWN
            elif f_health <= record['fail_health']:
                continue
            elif f_health >= record['win_health']:
                follower['status'] = const.FFR_MUST_WIN
                follower['arrangement'] = record['arrangement']
                final_follower = follower
                break
            else:
                follower['status'] = const.FFR_NOT_SURE
            if not final_follower:
                final_follower = follower

        return final_follower

    def is_mission_end(self, mission):
        """
            如果是垃圾任务，结束流程
        """
        reward = mission['reward']
        r_type = reward.get('type')
        is_end = r_type not in [const.MRT_ANIMA, const.MRT_GOLD, const.MRT_PET, const.MRT_BOX]
        return is_end

    def is_mission_worth(self, mission):
        """
            判断任务值不值得做
        """
        # TODO: add complex logic, judge by role config
        m_id = mission['id']
        reward = mission['reward']
        r_id, r_type = reward.get('id'), reward.get('type')

        if r_id and r_type == const.MRT_BOX:
            for _id in r_id.split():
                item = reward_list.get(_id)
                if item:
                    r_type = item['type']
                    break

        cost = global_mission_list[m_id]['cost']
        anima = self.role_data['anima']

        if cost > anima - 4:
            return False
        mission['reward']['type'] = r_type
        if r_type in [const.MRT_GOLD, const.MRT_ANIMA, const.MRT_PET]:  # TODO: seed, reputation
            return True
        return False

    def get_next_role(self, role, role_list):
        if role not in role_list:
            raise VPException(f'get next role failed, role {role} not in role list {role_list}')
        if role_list[-1] == role:
            return role_list[0]
        return role_list[role_list.index(role) + 1]

    def get_arrangement_by_plugin(self, follower):
        plugin_control.assign_one_follower(follower['index'])
        plugin_control.calculate_arrangement()

        arrange = ''
        pattern = message_patterns.get(const.MT_MISSION_RESULT)
        for i in range(10):
            text = self.get_message(clear=False)
            result = pattern.findall(text)
            if result:
                arrange = result[-1]
                break

        if arrange and arrange[0] in '012x':
            return arrange
        else:
            return ''

    def add_mission_field(self, mission):
        if mission['id'] not in global_mission_list:
            return None
        m_info = global_mission_list.get(mission['id'])
        mission['name'] = m_info['name']
        mission['cost'] = m_info['cost']
        return mission


