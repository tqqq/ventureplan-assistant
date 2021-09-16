# coding=utf-8

import threading

"""
    basic mouse/keyboard operation
"""


class DeviceManager:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

    def mouse_move(self, x, y):
        # TODO
        pass

    def mouse_click(self, x, y):
        # TODO
        pass

    def mouse_right_click(self, x, y):
        # TODO
        pass

    def mouse_scroll_up(self, x, y):
        # TODO
        pass

    def mouse_scroll_down(self, x, y):
        # TODO
        pass

    def kboard_click(self, key):
        # TODO
        pass

    def kboard_combine_click(self, key1, key2):
        # TODO
        pass


device_manager = DeviceManager()
