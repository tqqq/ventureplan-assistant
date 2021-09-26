# coding=utf-8

import threading
import time
from pynput.keyboard import Controller as KBController, Key, KeyCode
from pynput.mouse import Controller as MouseController, Button

from vp_manager.config.account import system
from vp_manager.config.const import SYSTEM_MAC, SYSTEM_WIN
from vp_manager.utils.exceptions import VPException

"""
    basic mouse/keyboard operation
"""
kb_controller = KBController()
ms_controller = MouseController()

KEY_MAP = {
    'up': Key.up,
    'down': Key.down,
    'enter': Key.enter,
    'esc': Key.esc,
    'alt': Key.alt,
    'ctrl': Key.ctrl if system == SYSTEM_WIN else Key.cmd,
    # 'up': Key.up,
    # 'up': Key.up,
}


class DeviceManager:

    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

    def _get_key(self, key):
        if len(key) == 1:
            k = KeyCode.from_char(key)
        else:
            k = KEY_MAP.get(key)
            if not k:
                raise VPException(f'Unsupported key: {key}')
        return k

    def mouse_move(self, x, y):
        ms_controller.position = (x, y)

    def mouse_click(self, x, y):
        ms_controller.position = (x, y)
        time.sleep(0.1)
        ms_controller.click(Button.left)

    def mouse_right_click(self, x, y):
        ms_controller.position = (x, y)
        time.sleep(0.1)
        ms_controller.click(Button.right)

    def mouse_scroll_up(self):
        ms_controller.scroll(0, 3)

    def mouse_scroll_down(self):
        ms_controller.scroll(0, -3)

    def kboard_click(self, key):
        items = key.split('+')
        if len(items) == 2:
            self.kboard_combine_click(items[0], items[1])
            return

        k = self._get_key(key)
        kb_controller.press(k)
        kb_controller.release(k)

    def kboard_long_lick(self, key):
        k = self._get_key(key)

        kb_controller.press(k)
        time.sleep(0.5)
        kb_controller.release(k)

    def kboard_combine_click(self, key1, key2):
        k1 = self._get_key(key1)
        k2 = self._get_key(key2)

        kb_controller.press(k1)
        kb_controller.press(k2)
        kb_controller.release(k2)
        kb_controller.release(k1)


device_manager = DeviceManager()


def test():

    time.sleep(3)
    # device_manager.kboard_combine_click('ctrl', 'c')
    device_manager.kboard_click('esc')
    time.sleep(1)
    # # device_manager.kboard_click('enter')
    # time.sleep(1)
    # device_manager.kboard_long_lick('1')
    # time.sleep(1)
    # device_manager.kboard_long_lick('1')


if __name__ == '__main__':
    test()
