import logging
import sys
from functools import lru_cache

from foxylib.tools.log.logger_tool import LoggerTool, FoxylibLogFormatter
from foxylib.tools.url.url_tool import URLTool


class DiscordMessage:
    @classmethod
    def message2channel(cls, message):
        return message.channel


class DiscordTool:
    @classmethod
    def str2url_escaped(cls, str_in):
        str_out = URLTool.pattern().sub(r'<\1>', str_in)
        return str_out

    @classmethod
    def user_message2is_author(cls, user, message):
        return message.author == user


class DiscordLogger:
    ROOTNAME = "discord"

    @classmethod
    def rootname_list(cls):
        return [cls.ROOTNAME]

    @classmethod
    def attach_handler2loggers(cls, handler):
        for rootname in cls.rootname_list():
            logger = logging.getLogger(rootname)
            LoggerTool.add_or_skip_handlers(logger, [handler])

    @classmethod
    @lru_cache(maxsize=2)
    def attach_stderr2loggers(cls, level):
        handler = LoggerTool.handler_formatter2formatted(logging.StreamHandler(sys.stderr),
                                                         FoxylibLogFormatter.formatter(),
                                                         )
        handler.setLevel(level)
        cls.attach_handler2loggers(handler)


    # @classmethod
    # def func2name(cls, func):
    #     return LoggerTool.rootname_func2name(cls.ROOTNAME, func)
    #
    # @classmethod
    # def func_level2logger(cls, func, level):
    #     logger = logging.getLogger(cls.func2name(func))
    #     logger.setLevel(level)
    #     return logger
