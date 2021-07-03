import logging
from functools import wraps, partial

import nose

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.clazz.class_tool import cls2name


class ProfileTool:
    LEVEL_DEFAULT = logging.INFO

    @classmethod
    def _timedelta2message(cls, td_duration):
        ms = td_duration.total_seconds() * 1000
        return {"{}.duration".format(cls2name(cls)): "{0:.1f} ms".format(ms)}

    @classmethod
    def func2wrapped_with_duration(cls, func):
        import time

        @wraps(func)
        def wrapped(*_, **__):
            time_start = time.time()
            result = func(*_, **__)
            time_end = time.time()
            secs_execution = time_end - time_start

            return secs_execution, result

        return wrapped

    @classmethod
    def secs_func2dict_message(cls, secs, func):
        return {
            'message': f'[{cls.func2secs_logged.__qualname__}] {func.__qualname__}:{secs:.3f}s',
            'function': func.__qualname__,
            'secs': secs,
        }

    @classmethod
    def func2secs_logged(cls, func, secs_func2log=None,):
        def secs2log_default(secs):
            logger = FoxylibLogger.func_level2logger(cls.func2secs_logged, logging.DEBUG)
            logger.debug(cls.secs_func2dict_message(secs, func))

        secs2log = partial(secs_func2log, func=func) if secs_func2log else secs2log_default

        @wraps(func)
        def wrapped(*_, **__):
            secs, result = cls.func2wrapped_with_duration(func)(*_, **__)
            secs2log(secs)
            return result

        return wrapped
