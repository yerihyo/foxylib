from __future__ import absolute_import

import logging
from datetime import datetime

import pytz
from cachetools.keys import hashkey
# from cachetools import cached, lru, ttl
from nose.tools import assert_is_not_none

from foxylib.tools.cache.asymmetric_cache import AsymmetricCache
from foxylib.tools.cache.cache_tool import CacheTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class DatetimedCache:
    @classmethod
    def key_pivot2reader(cls, key, f_pivot):

        def reader(cache, *_, **__):
            logger = FoxylibLogger.func_level2logger(reader, logging.DEBUG)

            k = key(*_, **__)
            # raise Exception({"k":k})

            v, dt_created = cache[k]

            dt_pivot = f_pivot(*_, **__)

            # logger.debug({"k":k, "v":v, "dt_created":dt_created, "dt_pivot":dt_pivot})

            if dt_pivot > dt_created:
                raise KeyError(k)

            return v

        return reader

    @classmethod
    def key2writer(cls, key):
        def writer(cache, value, *_, **__):
            k = key(*_, **__)
            dt_now = datetime.now(pytz.utc)
            cache[k] = (value, dt_now)
        return writer

    @classmethod
    def _lookup_or_cache(cls, cache, k, lock, dt_pivot, func):
        try:
            v, dt_created = CacheTool.key2get(cache, k, lock=lock)
            if dt_pivot <= dt_created:
                return v
        except KeyError:
            pass  # key not found

        v = func(*_, **__)

        try:
            dt_now = datetime.now(pytz.utc)
            CacheTool.key2set(cache, k, (v, dt_now), lock=lock)
            cache[k] = v
        except ValueError:
            pass  # value too large

        return v

    class Decorator:
        @classmethod
        def cached(cls, func=None, cache=None, key=None, f_pivot=None, lock=None, ):
            logger = FoxylibLogger.func_level2logger(cls.cached, logging.DEBUG)

            assert_is_not_none(cache)
            assert_is_not_none(f_pivot)

            key = key or hashkey
            reader = DatetimedCache.key_pivot2reader(key, f_pivot)
            writer = DatetimedCache.key2writer(key)

            return AsymmetricCache.Decorator.cached(func=func, cache=cache, reader=reader, writer=writer, lock=lock)

        @classmethod
        def cachedmethod(cls, func=None, self2cache=None, key=None, f_pivot=None, lock=None, ):
            logger = FoxylibLogger.func_level2logger(cls.cachedmethod, logging.DEBUG)

            assert_is_not_none(self2cache)
            assert_is_not_none(f_pivot)

            key = key or hashkey
            reader = DatetimedCache.key_pivot2reader(key, f_pivot)
            writer = CacheTool.key2writer_default(key)

            return AsymmetricCache.Decorator.cachedmethod(func=func, self2cache=self2cache,
                                                          reader=reader, writer=writer, lock=lock)


