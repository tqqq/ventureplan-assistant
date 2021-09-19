# coding=utf-8

import os
from logging.config import dictConfig
from vp_manager.utils.log import LOG_CONFIG

if not os.path.exists('logs'):
    os.mkdir('logs')
dictConfig(LOG_CONFIG)


def main():
    from vp_manager.engine.core import Engine

    engine = Engine()
    engine.start()  # TODO: threading


if __name__ == '__main__':
    main()

