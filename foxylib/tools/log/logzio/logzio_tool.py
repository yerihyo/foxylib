import logging
from functools import lru_cache

from logzio.handler import LogzioHandler

# https://app.logz.io/#/dashboard/send-your-data/log-sources/python
class LogzioTool:
    @classmethod
    def formatter_default(cls):
        formatter = logging.Formatter(
            # fmt={"additional_field": "value"},
            fmt='{"additional_field": "value"}',
            validate=False)
        return formatter

    @classmethod
    def level_default(cls):
        return logging.INFO

    @classmethod
    def token2handler(cls, token):
        handler = LogzioHandler(token, logs_drain_timeout=5)
        handler.setFormatter(cls.formatter_default())
        # handler.setLevel(level)
        return handler
