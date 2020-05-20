import logging
from functools import wraps
from types import FunctionType, MethodType

import cachetools
from cachetools.keys import hashkey
from nose.tools import assert_equal, assert_is_not_none

from foxylib.tools.cache.cache_tool import CacheTool
from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.function.method_tool import MethodTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import AttributeTool


class CacheManager:
    class Constant:
        ATTRIBUTE_NAME = "CacheManager"

    class Field:
        CACHE = "cache"
        KEY = "key"
        LOCK = "lock"

    @classmethod
    def manager2cache(cls, manager):
        return manager[cls.Field.CACHE]

    @classmethod
    def manager2key(cls, manager):
        return manager[cls.Field.KEY]

    @classmethod
    def manager2lock(cls, manager):
        return manager[cls.Field.LOCK]

    # def __init__(self, cache, key, lock=None):
    #     self.cache = cache
    #     self.key = key
    #     self.lock = lock

    @classmethod
    def add2cache(cls, manager, obj, args=None, kwargs=None,):
        key, cache, lock = cls.manager2key(manager), cls.manager2cache(manager), cls.manager2lock(manager)

        k = key(*(args or []), **(kwargs or {}))
        CacheTool.cache_key2set(cache, k, obj, lock=lock)

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
    def callable2cache(cls, callable):
        return cls.manager2cache(cls.callable2manager(callable))

    @classmethod
    def func2manager(cls, func):
        return getattr(func, cls.Constant.ATTRIBUTE_NAME)

    @classmethod
    def method2manager(cls, method):
        logger = FoxylibLogger.func_level2logger(cls.method2manager, logging.DEBUG)

        # logger.debug({"method.__self__": method.__self__,
        #               "method": method,
        #               "method.__name__": method.__name__,
        #               })

        h_manager = cls.object2h_manager(MethodTool.method2owner(method))
        if not h_manager:
            return None

        return h_manager.get(method)


    @classmethod
    def attach2func(cls, func=None, cache=None, key=None, lock=None,):
        assert_is_not_none(cache)

        # if cached is None:
        #     cached = cachetools.cached

        if key is None:
            key = cachetools.keys.hashkey

        def wrapper(f):
            manager = {cls.Field.CACHE: cache,
                       cls.Field.KEY: key,
                       cls.Field.LOCK: lock,
                       }
            setattr(f, cls.Constant.ATTRIBUTE_NAME, manager)
            return f

        return wrapper(func) if func else wrapper

    # @classmethod
    # def attach_self2cache_objcac(cls, obj, self2cache,):
    #     h_manager = cls.object2h_manager(obj)
    #     manager = DictTool.get_or_init_lazy(h_manager, f.__name__, lambda: cls(self2cache(obj), key, lock))

    @classmethod
    def attach2method(cls, func=None, self2cache=None, key=None, lock=None, ):
        logger = FoxylibLogger.func_level2logger(cls.attach2method, logging.DEBUG)

        assert_is_not_none(self2cache)
        key = key or hashkey

        def wrapper(f):
            @wraps(f)
            def wrapped(self, *_, **__):
                # make sure we get the same cache for same 'self'
                h_manager = cls.object2h_manager(self)
                manager_raw = {cls.Field.CACHE: self2cache(self),
                               cls.Field.KEY: key,
                               cls.Field.LOCK: lock,
                               }

                method = MethodTool.owner_function2method(self, f)
                manager = DictTool.get_or_init_lazy(h_manager, method, lambda: manager_raw)

                # logger.debug({"self": self, "f": f, "h_manager": h_manager, "manager": manager})
                # logger.debug({"cls.object2h_manager(self)":cls.object2h_manager(self)})
                return f(self, *_, **__)

            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def cachedmethod2use_manager(cls, func=None, cachedmethod=None, method2manager=None):
        logger = FoxylibLogger.func_level2logger(cls.cachedmethod2use_manager, logging.DEBUG)

        assert_is_not_none(cachedmethod)
        method2manager = method2manager if method2manager else cls.method2manager

        def wrapper(f):
            @wraps(f)
            def wrapped(self, *_, **__):
                manager = method2manager(MethodTool.owner_function2method(self, f))
                cache, key, lock = cls.manager2cache(manager), cls.manager2key(manager), cls.manager2lock(manager)
                # logger.debug({"hex(id(cache))":hex(id(cache)), "manager":manager, })

                f_with_cache = cachedmethod(lambda x: cache, key=key, lock=lock)(f)
                # logger.debug({"cls.object2h_manager(self)":cls.object2h_manager(self)})
                return f_with_cache(self, *_, **__)

            return wrapped

        return wrapper(func) if func else wrapper


    # @classmethod
    # def attach2method_OLD(cls, func=None, cachedmethod=None, self2cache=None, key=None, lock=None,):
    #     logger = FoxylibLogger.func_level2logger(cls.attach2method_OLD, logging.DEBUG)
    #
    #     assert_is_not_none(self2cache)
    #     cachedmethod = cachedmethod if cachedmethod else cachetools.cachedmethod
    #     key = key if key else cachetools.keys.hashkey
    #
    #     def wrapper(f):
    #         @wraps(f)
    #         def wrapped(self, *_, **__):
    #             f2 = cls.attach2method(func=f, self2cache=self2cache, key=key, lock=lock)
    #             manager = cls.method2manager(f2)
    #
    #             f_with_cache = cachedmethod(lambda x: manager.cache, key=key, lock=lock)(f)
    #             # logger.debug({"cls.object2h_manager(self)":cls.object2h_manager(self)})
    #             return f_with_cache(self, *_, **__)
    #
    #         return wrapped
    #
    #     return wrapper(func) if func else wrapper
