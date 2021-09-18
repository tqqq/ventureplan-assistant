# coding=utf-8

import pynput
import time


def get_position():
    # print position after 4 seconds
    ctrl = pynput.mouse.Controller()

    time.sleep(4)
    print(ctrl.position)


def test_position(x, y):
    # move to position after 4 seconds
    ctrl = pynput.mouse.Controller()

    time.sleep(4)
    print(f'{x}, {y}')
    ctrl.position = (x, y)


if __name__ == '__main__':
    dx, dy = 212, 91
    get_position()
    # test_position(dx, dy)

