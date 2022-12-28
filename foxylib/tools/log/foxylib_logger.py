import logging
import os
import sys
from functools import reduce, lru_cache

from foxylib.tools.log.logger_tool import LoggerTool, FoxylibLogFormatter

FILE_PATH = os.path.realpath(__file__)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 3, FILE_PATH)


class FoxylibLogger:
    rootname = os.path.basename(REPO_DIR)

    # level = logging.DEBUG

    @classmethod
    def rootname_list(cls):
        return [cls.rootname, ]

    @classmethod
    def func2name(cls, func):
        return LoggerTool.rootname_func2name(cls.rootname, func)

    @classmethod
    def func_level2logger(cls, func, level):
        logger = logging.getLogger(cls.func2name(func))
        logger.setLevel(level)
        return logger

    # @classmethod
    # def func2logger(cls, func):
    #     return cls.func_level2logger(func, cls.level)

    @classmethod
    def attach_handler2loggers(cls, handler):
        for rootname in cls.rootname_list():
            logger = logging.getLogger(rootname)
            LoggerTool.logger2handler_attached(logger, handler)

    @classmethod
    @lru_cache(maxsize=1)
    def attach_stderr2loggers(cls, level):
        handler = cls.handler_stderr()
        handler.setLevel(level)
        cls.attach_handler2loggers(handler)

    @classmethod
    def handler_stderr(cls):
        return FoxylibLogFormatter.handler2formatter_set(
            logging.StreamHandler(sys.stderr)
        )
