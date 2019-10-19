import logging
from datetime import datetime
from functools import wraps

import nose

from foxylib.tools.native.class_tools import cls2name


class ProfileTool:
    LEVEL_DEFAULT = logging.INFO

    @classmethod
    def _timedelta2message(cls, td_duration):
        ms = td_duration.total_seconds() * 1000
        return {"{}.duration".format(cls2name(cls)): "{0:.1f} ms".format(ms)}

    @classmethod
    def wrapper_time(cls, func=None, timedelta2message=None, func2logger=None, level=None, ):
        nose.tools.assert_is_not_none(func2logger)
        level = level if level is not None else cls.LEVEL_DEFAULT
        timedelta2message = timedelta2message or cls._timedelta2message

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                logger = func2logger(f)

                dt_start = datetime.now()
                result = f(*args, **kwargs)
                td_exec = datetime.now() - dt_start

                message = timedelta2message(td_exec)
                logger.log(level, message)
                return result

            return wrapped

        return wrapper(func) if func else wrapper
