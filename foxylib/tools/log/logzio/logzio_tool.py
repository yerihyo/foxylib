import logging
from functools import lru_cache

from logzio.handler import LogzioHandler


class LogzioTool:
    @classmethod
    def formatter_default(cls):
        formatter = logging.Formatter(
            fmt={"additional_field": "value"},
            validate=False)
        return formatter

    @classmethod
    def level_default(cls):
        return logging.INFO

    @classmethod
    def token2handler(cls, token):
        handler = LogzioHandler(token)
        handler.setFormatter(cls.formatter_default())
        # handler.setLevel(level)
        return handler
