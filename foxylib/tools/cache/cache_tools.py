import json
import os
import sys
from functools import wraps

import six
from frozendict import frozendict
from nose.tools import assert_is_not_none

from foxylib.tools.file.file_tools import FileToolkit
from foxylib.tools.log.logger_tools import FoxylibLogger


class CacheToolkit:
    @classmethod
    def func_pair_identical(cls):
        f = lambda x:x
        return (f,f)

    class JSON:
        @classmethod
        def func_pair(cls):
            return (cls.serialize, cls.deserialize)

        @classmethod
        def normalize(cls, j):
            if isinstance(j, dict):
                return frozendict({k:cls.normalize(v) for k,v in sorted(j.items())})

            if isinstance(j, list):
                return tuple([cls.normalize(x) for x in j])

            return j

        @classmethod
        def serialize(cls, j):
            logger = FoxylibLogger.func2logger(cls.serialize)

            j_norm = cls.normalize(j)
            # print({"j":j, "j_norm":j_norm}, file=sys.stderr)
            logger.debug({"j":j, "j_norm":j_norm})

            return j_norm

        @classmethod
        def deserialize(cls, s):
            return s


    @classmethod
    def cache2hashable(cls, func=None, cache=None, f_pair=None,):
        assert_is_not_none(cache)
        assert_is_not_none(f_pair)

        f_serialize, f_deserialize = f_pair

        def wrapper(func):
            def deserialize_and_func(*args, **kwargs):
                _args = tuple([f_deserialize(arg) for arg in args])
                _kwargs = {k: f_deserialize(v) for k, v in six.viewitems(kwargs)}
                return func(*_args, **_kwargs)

            cached_func = cache(deserialize_and_func)

            @wraps(func)
            def wrapped(*args, **kwargs):
                _args = tuple([f_serialize(arg) for arg in args])
                _kwargs = {k: f_serialize(v) for k, v in kwargs.items()}
                return cached_func(*_args, **_kwargs)

            wrapped.cache_info = cached_func.cache_info
            wrapped.cache_clear = cached_func.cache_clear
            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def cache_utf82file(cls, func=None, filepath=None,):
        assert_is_not_none(filepath)

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if os.path.exists(filepath):
                    utf8_cached = FileToolkit.filepath2utf8(filepath)
                    return utf8_cached

                utf8 = f(*args,**kwargs)
                FileToolkit.utf82file(utf8, filepath)

                return utf8

            return wrapped

        return wrapper(func) if func else wrapper
