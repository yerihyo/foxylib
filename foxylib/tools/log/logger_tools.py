import copy
import logging
import os
from datetime import datetime
from functools import wraps, reduce
from logging.handlers import RotatingFileHandler

import nose

from foxylib.tools.function.function_tools import FunctionToolkit

FILE_PATH = os.path.realpath(__file__)
FOXYLIB_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_PATH)

class LoggerToolkit:
    instance = None
    @classmethod
    def level2str(cls, level):
        if level == logging.CRITICAL: return "critical"
        if level == logging.ERROR: return "error"
        if level == logging.WARNING: return "warning"
        if level == logging.INFO: return "info"
        if level == logging.DEBUG: return "debug"
        if level == logging.NOTSET: return "notset"
        raise Exception()

    @classmethod
    def format_python(cls):
        return "%(levelname)s:%(name)s:%(message)s"

    @classmethod
    def logger2flush_handlers(cls, logger):
        for h in logger.handlers:
            h.flush()
            
    @classmethod
    def add_or_skip_handlers(cls, logger, handlers):
        if not handlers: return

        for handler in (handlers or []):
            if handler in logger.handlers: continue

            logger.addHandler(handler)

    @classmethod
    def config2logger(cls, logger, config):
        if not config:
            return logger

        handlers = config.get("handlers")
        if handlers:
            for h in handlers:
                cls.add_or_skip_handlers(logger, h)

        level = config.get("level")
        if level is not None:
            logger.setLevel(level)

        return logger

    @classmethod
    def rootname_filename2logger(cls, rootname, filename, config=None):
        name = ".".join([rootname,filename])
        logger_raw = logging.getLogger(name)
        if config:
            logger = LoggerToolkit.config2logger(logger_raw, config=config)
        else:
            logger = logger_raw

        return logger

    @classmethod
    def rootname_func2logger(cls, rootname, func, config=None):
        from foxylib.tools.collections.collections_tools import lchain
        name = ".".join(lchain([rootname],FunctionToolkit.func2class_func_name_list(func)))
        logger_raw = logging.getLogger(name)
        if config:
            logger = LoggerToolkit.config2logger(logger_raw, config=config)
        else:
            logger = logger_raw

        return logger

    @classmethod
    def f_log2f_level(cls, f_log, level):
        def f_level(*args,**kwargs):
            kwargs_out = copy.deepcopy(kwargs)
            kwargs_out["level"] = level
            return f_log(*args, **kwargs_out)
        return f_level

    @classmethod
    def filepath2handler_default(cls, filepath,):
        handler = RotatingFileHandler(filepath, mode='a', maxBytes=5 * 1024 * 1024,
                                      backupCount=2, encoding="utf-8", delay=False)
        return handler

    @classmethod
    def handler2formatted(cls, handler, ):
        formatter = LoggerToolkit.Foxytrixy.formatter()
        handler.setFormatter(formatter)
        return handler

    # @classmethod
    # def _attach_handler2logger(cls, handler, logger_name, ):
    #     logger = logging.getLogger(logger_name)
    #     LoggerToolkit.add_or_skip_handlers(logger, [handler])


    class SEWrapper:
        @classmethod
        def level_default(cls): return logging.INFO

        @classmethod
        def log(cls, func=None, func2logger=None, level=None, ):
            nose.tools.assert_is_not_none(func2logger)

            def wrapper(f):
                @wraps(f)
                def wrapped(*args, **kwargs):
                    logger = func2logger(f)

                    _level = level if level is not None else cls.level_default()

                    dt_start = datetime.utcnow()
                    logger.log(_level, {"title":"START"})
                    result = f(*args, **kwargs)
                    td_exec = datetime.utcnow() - dt_start
                    logger.log(_level, {"title":"END", 'millisec': round(td_exec.total_seconds() * 1000, 3),})

                    return result

                return wrapped

            return wrapper(func) if func else wrapper

        @classmethod
        def info(cls, *a, **k): return LoggerToolkit.f_log2f_level(cls.log, logging.INFO)(*a, **k)


    class DurationWrapper:
        @classmethod
        def level_default(cls): return logging.INFO

        @classmethod
        def log(cls, func=None, msg_title=None, func2logger=None, level=None,):
            nose.tools.assert_is_not_none(func2logger)

            def wrapper(f):
                @wraps(f)
                def wrapped(*args, **kwargs):
                    logger = func2logger(f)

                    _level = level if level is not None else cls.level_default()
                    _msg_title = msg_title if msg_title is not None else "exec duration"

                    dt_start = datetime.now()
                    result = f(*args, **kwargs)
                    td_exec = datetime.now() - dt_start

                    msg = {
                        'title': _msg_title,
                        'millisec': round(td_exec.total_seconds() * 1000, 3),
                    }
                    logger.log(_level,msg)
                    return result

                return wrapped

            return wrapper(func) if func else wrapper

        @classmethod
        def info(cls, *a, **k): return LoggerToolkit.f_log2f_level(cls.log, logging.INFO)(*a, **k)

    class Foxytrixy:
        @classmethod
        def format(cls):
            # return "%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:#%(lineno)s:%(message)s"
            return "%(asctime)s.%(msecs)03d:%(levelname)s:%(filename)s#%(lineno)s:%(name)s:%(message)s"
            # return "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s:%(funcName):%(message)s"
            # return "%(asctime)s:%(levelname)s:%(filename)s#%(lineno)s:%(name):%(message)s"

        @classmethod
        def datefmt(cls):
            from foxylib.tools.date.date_tools import DatetimeToolkit
            return DatetimeToolkit.iso8601()

        @classmethod
        def config(cls):
            h = {"format": cls.format(),
                 "datefmt": cls.datefmt(), }
            return h

        @classmethod
        def formatter(cls):
            return logging.Formatter(cls.format(), cls.datefmt())

class FoxylibLogger:
    ROOTNAME = os.path.basename(FOXYLIB_DIR)
    level = logging.DEBUG


    @classmethod
    def func2logger(cls, *args, **kwargs):
        logger = LoggerToolkit.rootname_func2logger(cls.ROOTNAME, *args, **kwargs)
        logger.setLevel(cls.level)
        return logger

# class LoggerToolkit:
#     _me = None
#     def __init__(self):
#         self.handlers = None
#         self.level = None
#
#     @classmethod
#     def me(cls):
#         if not cls._me:
#             cls._me = cls()
#         return cls._me
#
#     def func2logger(self, func,):
#         name = LoggerToolkit.func2name(func)
#         logger = logging.getLogger(name)
#
#         if self.handlers:
#             LoggerToolkit.add_or_skip_handlers(logger, self.handlers)
#
#         if self.level is not None:
#             logger.setLevel(logger)
#
#         return logger
#
#     @classmethod
#     def log_exec_duration(cls, func=None, msg=None, logger=None, ):
#         def wrapper(f):
#             @wraps(f)
#             def wrapped(*args, **kwargs):
#                 _logger = cls.me().func2logger(f) if logger is None else logger
#                 _msg = "[{0}] exec time".format(FunctionToolkit.func2name(f)) if msg is None else msg
#
#                 dt_start = datetime.now()
#                 result = f(*args, **kwargs)
#                 td_exec = datetime.now() - dt_start
#
#                 _logger.info({
#                     'message': _msg,
#                     'exec_ms': round(td_exec.total_seconds() * 1000, 3),
#                 })
#                 return result
#
#             return wrapped
#
#         return wrapper(func) if func else wrapper






