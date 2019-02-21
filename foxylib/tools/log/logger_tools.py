import inspect
import logging
import os
from datetime import datetime
from functools import wraps

from foxylib.tools.native.class_tools import ClassToolkit
from foxylib.tools.native.function_tools import FunctionToolkit

class LoggerToolkit:
    @classmethod
    def level2str(cls, level):
        if level == logging.CRITICAL: return "critical"
        if level == logging.ERROR: return "error"
        if level == logging.WARNING: return "warning"
        if level == logging.INFO: return "info"
        if level == logging.DEBUG: return "debug"
        if level == logging.NOTSET: return "notset"
        raise Exception()

    # @classmethod
    # def add_handlers_and_return(cls, logger, handlers):
    #     for handler in handlers:
    #         logger.addHandler(handler)
    #     return logger

    @classmethod
    def func2name(cls, f):
        # filepath = inspect.getfile(f)
        # basename = os.path.splitext(os.path.basename(filepath))[0]
        l = [] #basename]

        clazz = FunctionToolkit.func2cls(f)
        if clazz: l.append(ClassToolkit.cls2name(clazz))
        l.append(FunctionToolkit.func2name(f))

        name = ".".join(l)
        return name

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
    def func2logger(cls, func, handlers=None, level=None,):
        name = cls.func2name(func)
        logger = logging.getLogger(name)

        cls.add_or_skip_handlers(logger, handlers)

        if level is not None:
            logger.setLevel(level)

        return logger




    # @classmethod
    # def _name2logger(cls, name):
    #     logger = logging.getLogger(name)
    #
    #     # required only during debugging?
    #
    #     if not logger.handlers:
    #         handler = logging.StreamHandler(stream=sys.stderr)
    #         handler.setLevel(logging.INFO)
    #         handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s', "%Y.%m.%d %H:%M:%S"))
    #         logger.addHandler(handler)
    #
    #     return logger

