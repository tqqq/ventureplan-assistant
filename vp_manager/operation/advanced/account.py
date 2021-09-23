# coding=utf-8
import logging
import time

from vp_manager.operation.basic import device_manager
from vp_manager.config import position, sleep_time, key_setting
from vp_manager.utils.exceptions import VPException

logger = logging.getLogger(__name__)


def choose_battle_account(index):
    with device_manager:
        device_manager.mouse_click(position.BATTLE_NET_WINDOW_X, position.BATTLE_NET_WINDOW_Y)
        time.sleep(0.5)
        device_manager.mouse_click(position.BATTLE_NET_WINDOW_X, position.BATTLE_NET_WINDOW_Y)
        time.sleep(0.5)
        device_manager.mouse_click(position.BN_CHOOSE_ACCOUNT_X, position.BN_CHOOSE_ACCOUNT_Y)
        time.sleep(0.5)
        x, y = position.BN_ACCOUNT[index]
        device_manager.mouse_click(x, y)
        time.sleep(0.5)


def open_client():
    with device_manager:
        device_manager.mouse_click(position.BATTLE_NET_WINDOW_X, position.BATTLE_NET_WINDOW_Y)
        time.sleep(0.05)
        device_manager.mouse_click(position.START_GAME_X, position.START_GAME_Y)
    time.sleep(sleep_time.AFTER_START_GAME)
    with device_manager:
        device_manager.mouse_click(position.GAME_WINDOW_X, position.GAME_WINDOW_Y)
    time.sleep(0.5)


def choose_role(role, current_role, role_list):
    if role == current_role:
        return

    if role not in role_list:
        raise VPException(f'target role {role} not in role list {role_list}')
    if current_role not in role_list:
        raise VPException(f'current role {role} not in role list {role_list}')

    target_index = role_list.index(role)
    current_index = role_list.index(current_role)

    if target_index > current_index:
        with device_manager:
            for i in range(target_index-current_index):
                device_manager.kboard_click('down')
                time.sleep(sleep_time.BETWEEN_SWITCH_ROLE)
    else:
        with device_manager:
            for i in range(current_index-target_index):
                device_manager.kboard_click('up')
                time.sleep(sleep_time.BETWEEN_SWITCH_ROLE)


def choose_server():
    # TODO
    pass


def enter_game():
    with device_manager:
        device_manager.kboard_click('enter')
    time.sleep(sleep_time.AFTER_LOGIN)


def logout():
    key = key_setting.KEY_LOGOUT
    with device_manager:
        device_manager.kboard_click(key)
    time.sleep(sleep_time.AFTER_LOGOUT)


def close_client():
    with device_manager:
        device_manager.mouse_click(position.CLOSE_GAME_X, position.CLOSE_GAME_Y)
    time.sleep(sleep_time.AFTER_CLOSE_GAME)


def print_role_info():
    key = key_setting.KEY_PRINT_ROLE_INFO
    with device_manager:
        device_manager.kboard_click(key)
    time.sleep(0.2)

