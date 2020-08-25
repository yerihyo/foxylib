from __future__ import absolute_import

import logging
from functools import wraps

# from cachetools import cached, lru, ttl
from nose.tools import assert_is_not_none, assert_in

from foxylib.tools.cache.cache_tool import CacheTool
from foxylib.tools.function.callable_tool import CallableTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import format_str


class AsymmetricCache:
    @classmethod
    def _read_or_write(cls, func, cache, reader, writer, *_, lock=None, **__):
        try:
            return CacheTool.reader2get(cache, reader, *_, lock=lock, **__)
        except KeyError:
            pass  # key not found

        v = func(*_, **__)

        try:
            CacheTool.writer2set(cache, writer, v, *_, lock=lock, **__, )
        except ValueError:
            pass  # value too large

        return v

    class Decorator:
        @classmethod
        def cached(cls, func=None, cache=None, reader=None, writer=None, lock=None, ):
            logger = FoxylibLogger.func_level2logger(cls.cached, logging.DEBUG)

            assert_is_not_none(cache)
            assert_is_not_none(reader)
            assert_is_not_none(writer)

            def wrapper(f):
                """
                CLASSMETHOD can used cached() too.
                But for simplicity of the system, CLASSMETHOD is forced to use cachedmethod
                """
                types_valid = {CallableTool.Type.FUNCTION, }
                assert_in(CallableTool.callable2type(f), types_valid,
                          format_str("For instancemethod, use attach_cachedmethod() instead. type:{}",
                                     CallableTool.callable2type(f))
                          )

                @wraps(f)
                def wrapped(*_, **__):
                    # raise Exception({"_":_, "__":__})

                    v = AsymmetricCache._read_or_write(f, cache, reader, writer, *_, lock=lock, **__)
                    return v

                return wrapped

            return wrapper(func) if func else wrapper

        @classmethod
        def cachedmethod(cls, func=None, self2cache=None, reader=None, writer=None, lock=None, ):
            logger = FoxylibLogger.func_level2logger(cls.cachedmethod, logging.DEBUG)

            assert_is_not_none(self2cache)

            def wrapper(f):
                """
                CLASSMETHOD can used cached() too.
                But for simplicity of the system, CLASSMETHOD is forced to use cachedmethod
                """
                types_valid = {CallableTool.Type.FUNCTION, }
                assert_in(CallableTool.callable2type(f), types_valid,
                          "For instancemethod, use attach_cachedmethod() instead")

                @wraps(f)
                def wrapped(self, *_, **__):
                    cache = self2cache(self)
                    v = AsymmetricCache._read_or_write(f, cache, reader, writer, *_, lock=lock, *__)
                    return v

                return wrapped

            return wrapper(func) if func else wrapper
