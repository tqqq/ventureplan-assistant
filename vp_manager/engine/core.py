# coding=utf-8
import queue
import json
import logging

from vp_manager.operation.advanced import vp as plugin_control, \
    account as account_control, copy_chat as copy_control
from vp_manager.config import account as account_config, const


logger = logging.getLogger(__name__)


class Engine:

    def __init__(self):  # TODO: muti window
        self.current_role = ''  # role name
        self.role_data = {}  # role name
        self.follower_data = {}  # follower_level, soldier level
        self.mission_list = []  # just record first 6 missions, mission id, name, type, time, cost, level, reward

    def start(self):
        while True:
            try:
                account_control.open_client()
                self.work()
            except Exception:
                pass
            account_control.close_client()

    def get_message(self, m_type, timeout=3):
        copy_control.open_window()
        text = copy_control.copy_text()
        copy_control.close_window()

        # TODO: parse text
        data = {'name': text}

        return data

    def work(self):

        role = self.current_role if self.current_role else account_config.efficient_role[0]

        while True:
            account_control.choose_role(role, self.current_role, account_config.total_role)
            account_control.enter_game()
            account_control.print_role_info()

            self.role_data = self.get_message(m_type=const.MT_ROLE_DATA, timeout=3)
            self.current_role = self.role_data['name']

            self.manage_missions()

            role = self.get_next_role(role, account_config.efficient_role)
            account_control.logout()

    def manage_missions(self):

        self.open_venture_plan()
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
        # TODO:
        # 1. click button into mission view
        # 2. print and get follower_data, mission_data
        # 3. calculate arrange by cache
        # 4. calculate arrange by plugin
        # 5. exit

        return const.MER_FAILED

    def get_next_role(self, role, role_list):
        # TODO
        return role

    def open_venture_plan(self):
        # TODO:
        # generate positions
        # loop click and get data from queue
        # store position
        pass












