# coding=utf-8
import logging
import time

import clipboard

from vp_manager.operation.basic import device_manager
from vp_manager.config import position, sleep_time, key_setting, const, account
from vp_manager.utils.exceptions import VPException

logger = logging.getLogger(__name__)


def open_window():
    with device_manager:
        device_manager.kboard_click(key_setting.KEY_OPEN_CCP_WINDOW)
    time.sleep(0.3)


def copy_text():
    with device_manager:
        device_manager.mouse_click(position.COPY_CHAT_WINDOW_X, position.COPY_CHAT_WINDOW_Y)
        time.sleep(0.1)
        device_manager.kboard_combine_click('ctrl', 'a')
        time.sleep(0.1)
        device_manager.kboard_combine_click('ctrl', 'c')
    time.sleep(0.1)
    text = _get_clipboard_data()

    return text


def close_window(clear):
    with device_manager:
        if clear:  # 中间close按钮 清空聊天栏
            device_manager.mouse_click(position.COPY_CHAT_CLOSE_CLEAR_X, position.COPY_CHAT_CLOSE_CLEAR_Y)
        else:  # 右上角X 保留聊天栏
            device_manager.mouse_click(position.COPY_CHAT_CLOSE_NO_CLEAR_X, position.COPY_CHAT_CLOSE_NO_CLEAR_Y)
        # time.sleep(0.2)


def _get_clipboard_data():

    data = clipboard.paste()
    clipboard.copy('trash data')

    return str(data)


def test():
    import clipboard
    time.sleep(4)
    c = clipboard.paste()
    print(c)
    clipboard.copy('hahaha')
    c = clipboard.paste()
    print(c)


# if __name__ == '__main__':
#     test()
