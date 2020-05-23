import logging
from functools import wraps, partial

import cachetools
from future.utils import lmap
from nose.tools import assert_is_not_none

from foxylib.tools.cache.cache_tool import CacheBatchTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class CacheDecorator:
    @classmethod
    def cachedmethod_each(cls, self2cache, indexes_each, key=cachetools.keys.hashkey, lock=None):
        logger = FoxylibLogger.func_level2logger(cls.cachedmethod_each, logging.DEBUG)

        """Decorator to wrap a function with a memoizing callable that saves
        results in a cache for each obj given a list of objects.

        Motivated by cachetools.cached
        """
        assert_is_not_none(self2cache)
        assert_is_not_none(indexes_each)

        indexes_each_no_self = lmap(lambda x:x-1, indexes_each)

        def wrapper(f_batch):
            @wraps(f_batch)
            def wrapped(self, *args, **kwargs):
                cache = self2cache(self)
                # logger.debug({"hex(id(cache))": hex(id(cache))})
                return CacheBatchTool.batchrun(partial(f_batch, self), args, kwargs, cache,
                                               indexes_each_no_self, key, lock)

            return wrapped

        return wrapper

    @classmethod
    def cached_each(cls, cache, indexes_each, key=cachetools.keys.hashkey, lock=None):
        logger = FoxylibLogger.func_level2logger(cls.cached_each, logging.DEBUG)

        """Decorator to wrap a function with a memoizing callable that saves
        results in a cache for each obj given a list of objects.

        Motivated by cachetools.cached
        """
        assert_is_not_none(cache)
        assert_is_not_none(indexes_each)

        def wrapper(f_batch):
            @wraps(f_batch)
            def wrapped(*args, **kwargs):
                return CacheBatchTool.batchrun(f_batch, args, kwargs, cache, indexes_each, key, lock)
            return wrapped

        return wrapper
