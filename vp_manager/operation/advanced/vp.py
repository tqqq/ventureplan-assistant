# coding=utf-8
import logging
import time

from vp_manager.operation.basic import device_manager
from vp_manager.config import position, sleep_time, key_setting
from vp_manager.utils.exceptions import VPException


logger = logging.getLogger(__name__)


def open_venture_plan():
    key1 = key_setting.KEY_SET_FIRST_VIEW
    with device_manager:
        device_manager.kboard_click(key1)
    time.sleep(0.8)

    key2 = key_setting.KEY_CORGI_TOY
    with device_manager:
        device_manager.kboard_click(key2)
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
    with device_manager:
        device_manager.mouse_click(position.CLOSE_MISSION_VIEW_X, position.CLOSE_MISSION_VIEW_Y)
    time.sleep(0.3)


def assign_one_follower(index):
    with device_manager:
        x, y = position.FOLLOWERS[index]
        device_manager.mouse_right_click(x, y)
        time.sleep(0.1)
    pass


def assign_follower_team(arrangement, index):
    """
    插件的站位:       右键上随从的顺序:
     2   3   4         1   2   3
       0   1             4   5
    """

    arrangement = arrangement.lower()
    reflect = [2, 3, 4, 0, 1]

    new_arrange = ''.join([arrangement[i] for i in reflect])


    with device_manager:
        for c in new_arrange:
            if c == '1' or c == '0':
                device_manager.mouse_right_click(position.SOLDIER_1_X, position.SOLDIER_1_Y)
                time.sleep(0.1)
            elif c == '2':
                device_manager.mouse_right_click(position.SOLDIER_2_X, position.SOLDIER_2_Y)
                time.sleep(0.1)
            elif c == 'x':
                x, y = position.FOLLOWERS[index]
                device_manager.mouse_right_click(x, y)
                time.sleep(0.1)
            else:
                device_manager.mouse_right_click(position.SOLDIER_1_X, position.SOLDIER_1_Y)
                time.sleep(0.1)
                logger.warning(f'unknown arrangement: {arrangement}')

        for i, c in enumerate(new_arrange):
            if c == '0':
                x, y = position.BATTLE_GROUND[i]
                device_manager.mouse_right_click(x, y)
                time.sleep(0.1)


def calculate_arrangement():
    with device_manager:
        device_manager.mouse_click(position.CALCULATE_BUTTON_X, position.CALCULATE_BUTTON_Y)
    time.sleep(sleep_time.AFTER_CALCULATE)


def confirm_mission():
    with device_manager:
        device_manager.mouse_click(position.CONFIRM_MISSION_X, position.CONFIRM_MISSION_Y)
    time.sleep(0.3)


def start_all_missions():
    with device_manager:
        device_manager.mouse_click(position.START_ALL_MISSIONS_X, position.START_ALL_MISSIONS_Y)
    time.sleep(sleep_time.AFTER_START_ALL_MISSIONS)


