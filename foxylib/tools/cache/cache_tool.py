from functools import wraps

import dill
import six
from frozendict import frozendict
from nose.tools import assert_is_not_none

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class CacheTool:
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

            if isinstance(j, (list,set)):
                return tuple([cls.normalize(x) for x in j])

            return j

        @classmethod
        def serialize(cls, v): return cls.serialize_natural(v)
        @classmethod
        def deserialize(cls, s): return cls.deserialize_natural(s)

        @classmethod
        def serialize_natural(cls, j): return cls.normalize(j)
        @classmethod
        def deserialize_natural(cls, s): return s

        @classmethod
        def serialize_dill(cls, j): return dill.dumps(cls.normalize(j))
        @classmethod
        def deserialize_dill(cls, s): return dill.loads(s)

    @classmethod
    def cache2hashable(cls, func=None, cache=None, f_pair=None,):

        assert_is_not_none(cache)
        assert_is_not_none(f_pair)

        f_serialize, f_deserialize = f_pair

        def wrapper(func):
            def deserialize_and_func(*args, **kwargs):
                logger = FoxylibLogger.func2logger(deserialize_and_func)
                _args = tuple([f_deserialize(arg) for arg in args])
                _kwargs = {k: f_deserialize(v) for k, v in six.viewitems(kwargs)}

                # logger.debug({"func": func, "args": args, "_args": _args, "kwargs": kwargs, "_kwargs": _kwargs, })
                return func(*_args, **_kwargs)

            cached_func = cache(deserialize_and_func)

            @wraps(func)
            def wrapped(*args, **kwargs):
                logger = FoxylibLogger.func2logger(wrapped)
                # logger.debug({"func": func, "args": args, "kwargs": kwargs, })

                _args = tuple([f_serialize(arg) for arg in args])
                _kwargs = {k: f_serialize(v) for k, v in kwargs.items()}
                return cached_func(*_args, **_kwargs)

            wrapped.cache_info = cached_func.cache_info
            wrapped.cache_clear = cached_func.cache_clear
            return wrapped

        return wrapper(func) if func else wrapper



