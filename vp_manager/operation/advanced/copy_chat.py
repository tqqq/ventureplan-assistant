# coding=utf-8
import logging
import time

from pynput.keyboard import Key

from vp_manager.operation.basic import device_manager
from vp_manager.config import position, sleep_time, key_setting
from vp_manager.utils.exceptions import VPException

logger = logging.getLogger(__name__)


def open_window():
    with device_manager:
        device_manager.mouse_click(position.COPY_CHAT_OPEN_X, position.COPY_CHAT_OPEN_Y)
    time.sleep(0.5)


def copy_text():
    with device_manager:
        device_manager.mouse_click(position.COPY_CHAT_WINDOW_X, position.COPY_CHAT_WINDOW_Y)
        time.sleep(0.1)
        device_manager.kboard_combine_click('ctrl', 'a')
        time.sleep(0.1)
        device_manager.kboard_combine_click('ctrl', 'c')
    time.sleep(0.2)


def close_window(clear):
    with device_manager:
        if clear:
            device_manager.mouse_click(position.COPY_CHAT_CLOSE_CLEAR_X, position.COPY_CHAT_CLOSE_CLEAR_Y)
        else:
            device_manager.mouse_click(position.COPY_CHAT_CLOSE_NO_CLEAR_X, position.COPY_CHAT_CLOSE_NO_CLEAR_Y)
        # time.sleep(0.2)

