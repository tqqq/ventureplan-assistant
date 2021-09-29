# coding=utf-8

import json
import logging
import re
import time

from vp_manager.operation.advanced import vp as plugin_control, \
    account as account_control, copy_chat as copy_control
from vp_manager.config import account as account_config, const
from vp_manager.utils.exceptions import VPException
from vp_manager.data import mission_list as global_mission_list
from vp_manager.data import follower_list as global_follower_list
from vp_manager.data import reward_list
from vp_manager.engine.database import get_win_arranges, update_arrangement

logger = logging.getLogger(__name__)

message_patterns = {
    const.MT_ROLE_DATA: re.compile(r'##ROLE_DATA##(.*?)##'),
    const.MT_MISSION_DATA: re.compile(r'##MISSION_DATA##(.*?)##'),
    const.MT_MISSION_RESULT: re.compile(r'##MISSION_RESULT##(.*?)##'),
    const.MT_FOLLOWER_INFO: re.compile(r'##FOLLOWER_INFO##(.*?)##'),
    const.MT_SOLDIER_LEVEL: re.compile(r'##SOLDIER_LEVEL##(\d+)##'),
    const.MT_MISSION_COMPLETED: re.compile(r'(MISSION_COMPLETED)'),
}


class Engine:

    def __init__(self):  # TODO: muti window
        self.current_role = account_config.efficient_role[0]  # role name
        self.role_data = {}  # role name, anima
        self.mission_list = []  # pre_assigned missions id

    def start(self, limit=-1):
        # while True:
        try:
            account_control.choose_battle_account(index=1)
            account_control.open_client()
            self.work(limit)
        except VPException as e:
            logger.error(e.msg)

        account_control.close_client()

    def get_message(self, clear=True):
        copy_control.open_window()
        text = copy_control.copy_text()
        copy_control.close_window(clear)

        return text

    def work(self, limit=-1):
        role = self.current_role
        if limit == -1:
            limit = 10000

        for i in range(limit*2):
            self.login(role)
            anima = self.role_data['anima']
            success = True
            if int(anima) < 100:
                logger.warning(f'{self.current_role} anima is {anima}, will skip this role')
            else:
                logger.info(f'{self.current_role} anima is {anima}, start manage missions')
                success = self.manage_missions()

            if i >= limit and role == account_config.efficient_role[0]:
                break

            if success:
                role = self.get_next_role(self.current_role, account_config.efficient_role)
            else:
                role = self.current_role
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
        pattern = message_patterns.get(const.MT_MISSION_COMPLETED)
        complete = False
        for i in range(5):
            text = self.get_message(clear=False)
            result = pattern.findall(text)
            if result:
                complete = True
                break
            time.sleep(2)
        if not complete:
            return False

        index = 0
        while index < 6:  # only do first 6 missions
            plugin_control.enter_mission_view(index)
            status = self.execute_mission(index)
            if status == const.MER_FAILED:
                plugin_control.close_mission_view()
                index += 1
            elif status == const.MER_END:
                plugin_control.close_mission_view()
                break

        self.mission_list = []
        plugin_control.start_all_missions()
        return True

    def execute_mission(self, index):
        """
        mission: {
            "id": "2300,
            "level": 48,
            "reward_id": "1234 1235"
        }

        follower_data: [
            {
                "id": "1236",
                "level": 47,
                "health": 1230
            },
            ...
        ]
        soldier_level: 47


        :param index:
        :return:
        """

        text = self.get_message()
        m_pattern = message_patterns.get(const.MT_MISSION_DATA)
        f_pattern = message_patterns.get(const.MT_FOLLOWER_INFO)
        s_pattern = message_patterns.get(const.MT_SOLDIER_LEVEL)

        try:
            mission = json.loads(m_pattern.findall(text)[-1])  # id, level
            followers = json.loads(f_pattern.findall(text)[-1])[:8]  # only search first 8 followers
            s_level = json.loads(s_pattern.findall(text)[-1])
        except IndexError:
            logger.warning(f'can not get mission data, will end scan.')
            return const.MER_END

        if not (mission and followers and s_level):
            logger.warning(f'can not get mission data, will end scan.')
            return const.MER_END

        m_id, m_level = mission['id'], mission['level']
        mission = self.add_mission_field(mission)
        if not mission:
            logger.warning(f"Unknown mission id: {m_id}")
            return const.MER_FAILED

        if mission['id'] in self.mission_list:
            plugin_control.confirm_mission()
            return const.MER_SUCCESS

        if self.is_mission_end(mission):
            logger.info(f'got trash mission, will end scan. {mission["id"]} {mission["name"]}')
            return const.MER_END

        if not self.is_mission_worth(mission, s_level):
            logger.info(f'got worthless mission, will skip it. {mission["id"]} {mission["name"]} {mission["type"]}')
            return const.MER_FAILED

        for i, follower in enumerate(followers):
            follower['index'] = i  # position

        if mission['type'] == const.MRT_EXP:
            if len(followers) <= 6:  # 随从数>6时派最低的5个
                return const.MER_FAILED
            arrangement = self.assign_xp_missions(followers)
            if arrangement:
                plugin_control.confirm_mission()
                self.mission_list.append(mission['id'])
                self.role_data['anima'] = self.role_data['anima'] - mission['cost'] - 4
                return const.MER_SUCCESS
            return const.MER_FAILED

        win_followers, unsure_followers = self.get_record_from_storage(mission, s_level,
                                                                       followers[:4])  # only search first 4 followers
        is_win = False
        if win_followers:
            is_win = True
            follower = win_followers[-1]  #
            logger.info(f'get arrangement by cache success, will arrange ({follower["level"]}) {follower["name"]} '
                        f'({follower["health"]}) for mission ({m_level}){mission["name"]}, arrangement is {follower["arrangement"]}')
            plugin_control.assign_follower_team(follower['arrangement'], follower['index'])
        elif unsure_followers:
            for follower in unsure_followers:
                arrange = self.get_arrangement_by_plugin(follower)
                follower['arrangement'] = arrange
                # TODO: update in new thread
                update_arrangement(mission=mission, follower=follower, s_level=s_level)
                if arrange:
                    is_win = True
                    logger.info(
                        f'get arrangement by plugin success, will arrange ({follower["level"]}) {follower["name"]} '
                        f'({follower["health"]}) for mission ({m_level}){mission["name"]}, arrangement is {arrange}')
                    break

        if not is_win:
            logger.info(f'mission ({m_level}){mission["name"]} will fail anyway')
            return const.MER_FAILED

        plugin_control.confirm_mission()
        self.mission_list.append(mission['id'])
        self.role_data['anima'] = self.role_data['anima'] - mission['cost'] - 4
        return const.MER_SUCCESS

    def get_record_from_storage(self, mission, s_level, followers):
        """
            followers: the first 4 followers
        """

        result = get_win_arranges(mission=mission, s_level=s_level, followers=followers)
        result = {item['f_id']: item for item in result}

        win_followers, unsure_followers = [], []

        for follower in followers:
            follower['name'] = global_follower_list[follower['id']]['name']
            f_id, f_health = follower['id'], follower['health']
            record = result.get(f_id)
            if not record:
                follower['status'] = const.FFR_UNKNOWN
                unsure_followers.append(follower)
            elif f_health <= record['fail_health']:
                continue
            elif f_health >= record['win_health']:
                follower['status'] = const.FFR_MUST_WIN
                follower['arrangement'] = record['arrangement']
                win_followers.append(follower)
            else:
                follower['status'] = const.FFR_NOT_SURE
                unsure_followers.append(follower)

        return win_followers, unsure_followers

    def is_mission_end(self, mission):
        """
            如果是垃圾任务(优先级低于箱子和战役)，结束流程
        """
        r_type = mission['type']
        is_end = r_type in [const.MRT_EQUIP, const.MRT_ASH, const.MRT_UNKNOWN, const.MRT_SEED]
        return is_end

    def is_mission_worth(self, mission, s_level):
        """
            判断任务值不值得做(高消耗/裁缝箱子/肉箱子/高等级战役)
        """
        # TODO: add complex logic, judge by role config
        m_id = mission['id']
        r_type = mission['type']
        cost = global_mission_list[m_id]['cost']
        anima = self.role_data['anima']

        if cost > anima - 4:
            return False

        if r_type == const.MRT_BATTLE:
            stage = global_mission_list[m_id]['stage']
            if stage == 60:
                return s_level == 60
            if stage == 48:  # 48 or 60
                return s_level > 45
            if stage == 36:
                return s_level > 35
            if stage == 24:
                return s_level > 25
            if stage == 12:
                return s_level > 10
            return False

        if r_type in [const.MRT_BOX_CLOTH, const.MRT_BOX_MEAT, const.MRT_BOX, const.MRT_RUNE]:
            return False
        if anima < 1000 and cost > 30:
            return False
        if anima < 5000 and cost > 50:
            return False
        return True

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
        for i in range(60):
            time.sleep(2)
            text = self.get_message(clear=False)
            result = pattern.findall(text)
            if result:
                arrange = result[-1]
                break

        if arrange and arrange[0] in '012x':
            return arrange
        else:
            plugin_control.remove_one_follower()
            plugin_control.confirm_mission()  # 清楚聊天栏
            return ''

    def assign_xp_missions(self, followers):
        for follower in followers[-5:]:
            plugin_control.assign_one_follower(follower['index'])

        plugin_control.calculate_arrangement()
        arrange = ''
        pattern = message_patterns.get(const.MT_MISSION_RESULT)
        for i in range(10):
            time.sleep(2)
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
        mid_str = str(mission['id'])
        if mid_str not in global_mission_list:
            return None
        mission['id'] = mid_str
        m_info = global_mission_list.get(mid_str)
        mission['name'] = m_info['name']
        mission['cost'] = m_info['cost']
        mission['type'] = m_info['type']

        r_ids = mission.get('reward_id')
        if r_ids:
            for r_id in r_ids.strip().split():
                r_type = reward_list.get(r_id)
                if r_type:
                    mission['type'] = r_type
                    break

        return mission
