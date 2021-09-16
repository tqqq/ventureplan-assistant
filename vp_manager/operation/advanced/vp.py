# coding=utf-8
import logging
import time

from vp_manager.operation.basic import device_manager
from vp_manager.config import position, sleep_time, key_setting
from vp_manager.utils.exceptions import VPException


def open_venture_plan():
    key = key_setting.KEY_CORGI_TOY
    with device_manager:
        device_manager.kboard_click(key)
    time.sleep(0.2)
    with device_manager:
        device_manager.mouse_click(position.COMMAND_TABLE_X, position.COMMAND_TABLE_Y)
    time.sleep(0.2)


def complete_missions():
    with device_manager:
        device_manager.mouse_click(position.COMPLETE_MISSIONS_X, position.COMPLETE_MISSIONS_Y)
    time.sleep(sleep_time.COMPLETE_MISSIONS)


def enter_mission_view(m_id):
    x, y = position.MISSION_POS_LIST[m_id]
    with device_manager:
        device_manager.mouse_click(x, y)
    time.sleep(0.5)


def close_mission_view():
    # TODO
    pass


def assign_one_follower():
    # TODO
    pass


def assign_follower_team():
    # TODO
    pass


def calcu_win_rate():
    # TODO
    pass


def confirm_mission():
    # TODO
    pass


def start_all_missions():
    # TODO
    pass


