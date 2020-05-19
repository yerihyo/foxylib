import logging
from functools import wraps, lru_cache, partial
from types import FunctionType, MethodType

import cachetools.keys
from future.utils import lfilter, lmap
from nose.tools import assert_is_not_none, assert_equal

from foxylib.tools.cache.cache_tool import CacheTool, CacheBatchTool
from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import AttributeTool
from foxylib.tools.string.string_tool import format_str


class CachetoolsToolDecorator:



    @classmethod
    def cachedmethod_each(cls, self2cache, indexes_each, key=cachetools.keys.hashkey, lock=None):
        logger = FoxylibLogger.func_level2logger(cls.cachedmethod_each, logging.DEBUG)

        """Decorator to wrap a function with a memoizing callable that saves
        results in a cache for each obj given a list of objects.

        Motivated by cachetools.cached
        """
        assert_is_not_none(self2cache)
        assert_is_not_none(indexes_each)

        def wrapper(f_batch):
            @wraps(f_batch)
            def wrapped(self, *args, **kwargs):
                cache = self2cache(self)
                return CacheBatchTool.batchrun(partial(f_batch, self), args, kwargs, cache, indexes_each, key, lock)

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

    # @classmethod
    # def attach2func(cls, func=None, cached=None, cache=None):
    #     assert_is_not_none(cached)
    #     assert_is_not_none(cache)
    #
    #     def wrapper(f):
    #         f.cache = cache
    #         return cached(cache)(f)
    #
    #     return wrapper(func) if func else wrapper


class CachetoolsTool:
    Decorator = CachetoolsToolDecorator
    @classmethod
    def key4classmethod(cls, key):
        return FunctionTool.shift_args(key, 1)

    @classmethod
    def key4objectmethod(cls, key):
        return FunctionTool.shift_args(key, 1)


class CachetoolsManager:
    class Constant:
        ATTRIBUTE_NAME = "CachetoolsManager"

    def __init__(self, cache, key, lock=None):
        self.cache = cache
        self.key = key
        self.lock = lock

    def add2cache(self, obj, args=None, kwargs=None,):
        k = self.key(*(args or []), **(kwargs or {}))
        CacheTool.cache_key2set(self.cache, k, obj, lock=self.lock)

    @classmethod
    def object2h_manager(cls, object):
        v = AttributeTool.get_or_init(object, cls.Constant.ATTRIBUTE_NAME, {})
        assert_equal(getattr(object, cls.Constant.ATTRIBUTE_NAME), v)
        return v

    @classmethod
    def callable2manager(cls, callable):
        if isinstance(callable, FunctionType):
            return cls.func2manager(callable)

        if isinstance(callable, MethodType):
            return cls.method2manager(callable)

        raise NotImplementedError("Unsupported callable: {} / {}".format(type(callable), callable))


    @classmethod
    def func2manager(cls, func):
        return getattr(func, cls.Constant.ATTRIBUTE_NAME)

    @classmethod
    def method2manager(cls, method):
        logger = FoxylibLogger.func_level2logger(cls.method2manager, logging.DEBUG)

        logger.debug({"method.__self__": method.__self__,
                      "method": method,
                      "method.__name__": method.__name__,
                      })

        h_manager = cls.object2h_manager(method.__self__)
        if not h_manager:
            return None

        return h_manager.get(method.__name__)


    @classmethod
    def attach2func(cls, func=None, cached=None, cache=None, key=None,):
        assert_is_not_none(cache)

        if cached is None:
            cached = cachetools.cached

        if key is None:
            key = cachetools.keys.hashkey

        def wrapper(f):
            setattr(f, cls.Constant.ATTRIBUTE_NAME, cls(cache, key,))
            return cached(cache, key=key,)(f)

        return wrapper(func) if func else wrapper

    @classmethod
    def attach2method(cls, func=None, cachedmethod=None, self2cache=None, key=None, lock=None,):
        logger = FoxylibLogger.func_level2logger(cls.attach2method, logging.DEBUG)

        assert_is_not_none(self2cache)
        cachedmethod = cachedmethod if cachedmethod else cachetools.cachedmethod
        key = key if key else cachetools.keys.hashkey

        def wrapper(f):
            @wraps(f)
            def wrapped(self, *_, **__):
                # make sure we get the same cache for same 'self'
                h_manager = cls.object2h_manager(self)
                manager = DictTool.get_or_init_lazy(h_manager, f.__name__, lambda: cls(self2cache(self), key, lock))

                logger.debug({"self":self, "f":f, "h_manager": h_manager,"manager":manager})
                f_with_cache = cachedmethod(lambda x: manager.cache, key=key, lock=lock)(f)
                logger.debug({"cls.object2h_manager(self)":cls.object2h_manager(self)})
                return f_with_cache(self, *_, **__)

            return wrapped

        return wrapper(func) if func else wrapper


class CooldownTool:
    class NotCallableException(Exception):
        pass

    @classmethod
    def invoke_or_cooldown_error(cls, cache_cooldown, key=None, lock=None,):
        key = key or cachetools.keys.hashkey

        def wrapper(f):
            f_wrapped = cachetools.cached(cache_cooldown, key=key, lock=lock)(f)

            @wraps(f)
            def wrapped(*_, **__):
                k = key(*_, **__)
                if k in cache_cooldown:
                    raise cls.NotCallableException()

                return f_wrapped(*_, **__)
            return wrapped
        return wrapper

    @classmethod
    def invoke_or_cooldown_error_cachedmethod(cls, cachedmethod, key=None, lock=None, ):
        key = key or cachetools.keys.hashkey

        def wrapper(f):
            f_wrapped = cachetools.cachedmethod(cachedmethod, key=key, lock=lock)(f)

            @wraps(f)
            def wrapped(self, *_, **__):
                k = key(*_, **__)
                if k in cachedmethod(self):
                    raise cls.NotCallableException()

                return f_wrapped(self, *_, **__)

            return wrapped

        return wrapper



# class MultilayercacheTool:
#     @classmethod
#     def cached(cls, cache_list):
#         def wrapper(f):
#             return reduce(lambda f, c: cached(c)(f), cache_list, f)
#
#         return wrapper
#
#     @classmethod
#     @IterTool.f_iter2f_list
#     def pop_depthspan(cls, cache_list, hashkey, depthspan, ):
#         for c in SpanTool.list_span2sublist(cache_list, depthspan):
#             yield c.pop(hashkey)
#
#     @classmethod
#     def pop(cls, cache_list, hashkey, ):
#         return cls.pop_depth_or_lower(cache_list, hashkey, 0)
#
#     @classmethod
#     def put(cls, cache_list, hashkey, value):
#         for c in cache_list:
#             c[hashkey] = value
#

