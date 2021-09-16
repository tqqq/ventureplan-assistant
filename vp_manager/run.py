# coding=utf-8

from logging.config import dictConfig

from vp_manager.engine.core import Engine
from vp_manager.utils.log import LOG_CONFIG


def main():
    dictConfig(LOG_CONFIG)

    engine = Engine()
    engine.start()  # TODO: threading


if __name__ == '__main__':
    main()

