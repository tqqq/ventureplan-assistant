# coding=utf-8

from logging.config import dictConfig
import logging
import os


LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(process)d:%(thread)d] %(filename)s[line:%(lineno)d]: %(message)s",
        }
    },
    "handlers": {
        "stream": {"class": "logging.StreamHandler", "formatter": "default"},
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": os.path.join("logs", "vp_manager.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
        },
    },
    "root": {
        "level": os.environ.get("log_level", "DEBUG"),
        "handlers": ["stream", "file"],
    },
}


def test():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    dictConfig(LOG_CONFIG)

    logger = logging.getLogger(__name__)
    logger.debug('hahaha')
