# coding=utf-8

import os
from logging.config import dictConfig
from vp_manager.utils.log import LOG_CONFIG

if not os.path.exists('logs'):
    os.mkdir('logs')
dictConfig(LOG_CONFIG)


def main():
    from vp_manager.engine.core import Engine
    from vp_manager.engine.pet_engine import PetEngine

    import time
    time.sleep(5)

    while True:
        engine1 = Engine()
        engine1.start(limit=21)  # TODO: threading

        engine2 = PetEngine()
        engine2.start()


if __name__ == '__main__':
    main()

