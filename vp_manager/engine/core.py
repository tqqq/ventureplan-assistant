# coding=utf-8

import json
import logging
import re

from vp_manager.operation.advanced import vp as plugin_control, \
    account as account_control, copy_chat as copy_control
from vp_manager.config import account as account_config, const
from vp_manager.utils.exceptions import VPException
from vp_manager.data.missions import mission_list
from vp_manager.data.rewards import reward_list

logger = logging.getLogger(__name__)

message_patterns = {
    const.MT_ROLE_DATA: re.compile(r'##ROLE_DATA##()##'),
    const.MT_MISSION_DATA: re.compile(r'##MT_MISSION_DATA##()##'),
    const.MT_MISSION_RESULT: re.compile(r'##MISSION_RESULT##()##'),
}


class Engine:

    def __init__(self):  # TODO: muti window
        self.current_role = account_config.efficient_role[0]  # role name
        self.role_data = {}  # role name
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

    def get_message(self):
        copy_control.open_window()
        text = copy_control.copy_text()
        copy_control.close_window()

        return text

    def work(self):
        role = self.current_role

        while True:
            self.login(role)
            self.manage_missions()

            role = self.get_next_role(self.current_role, account_config.efficient_role)
            account_control.logout()

    def login(self, role):
        account_control.choose_role(role, self.current_role, account_config.total_role)
        account_control.enter_game()
        account_control.print_role_info()

        text = self.get_message()
        pattern = message_patterns.get(const.MT_ROLE_DATA)
        if not pattern:
            raise VPException(f'wrong message type {const.MT_ROLE_DATA}')

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
        mission_data: {
            "id": 123,
            "level": 48,
            "reward": {
                "id": 1234,
                "type": "gold"
            }
        }

        follower_data: {
            "followers":[
                {
                    "id": 123,
                    "level": 47,
                    "health": 1230
                },
                ...
            ],
            "soldier_level": 47
        }

        :param index:
        :return:
        """
        # TODO:
        # 1. click button into mission view
        plugin_control.enter_mission_view(index)
        # 2. print and get follower_data, mission_data
        text = self.get_message()
        m_pattern = message_patterns.get(const.MT_MISSION_DATA)
        f_pattern = message_patterns.get(const.MT_FOLLOWER_INFO)
        mission_data = json.loads(m_pattern.findall(text)[-1])
        follower_data = json.loads(f_pattern.findall(text)[-1])

        m_id = mission_data['id']

        if not self.is_mission_worth(mission_data):
            return const.MER_END

        
        # 3. calculate arrange by cache
        # 4. calculate arrange by plugin
        # 5. exit

        return const.MER_FAILED

    def is_mission_worth(self, data):
        # TODO: add complex logic, judge by role config
        m_id = data['id']
        r_id = data['reward']['id']
        r_type = reward_list['id']

        return r_type in [const.MRT_GOLD, const.MRT_ANIMA, const.MRT_BOX_LEATHER, const.MRT_PET]

    def get_next_role(self, role, role_list):
        if role not in role_list:
            raise VPException(f'get next role failed, role {role} not in role list {role_list}')
        if role_list[-1] == role:
            return role_list[0]
        return role_list[role_list.index(role) + 1]














