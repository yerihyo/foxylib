import logging
from functools import wraps
from types import FunctionType, MethodType

import cachetools
from cachetools.keys import hashkey
from nose.tools import assert_is_not_none, assert_false, assert_true, assert_in

from foxylib.tools.cache.cache_tool import CacheTool
from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.callable_tool import CallableTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.function.method_tool import MethodTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import AttributeTool


class CacheManager:
    class Constant:
        ATTRIBUTE_NAME = "CacheManager"

    class Config:
        class Field:
            CACHE = "cache"
            SELF2CACHE = "self2cache"
            KEY = "key"
            LOCK = "lock"

        @classmethod
        def config2cache(cls, config):
            return config.get(cls.Field.CACHE)

        @classmethod
        def config2self2cache(cls, config):
            return config.get(cls.Field.SELF2CACHE)

        @classmethod
        def config2key(cls, config):
            return config[cls.Field.KEY]

        @classmethod
        def config2lock(cls, config):
            return config.get(cls.Field.LOCK)

        @classmethod
        def config2kwargs(cls, config):
            return DictTool.keys2excluded(config, [cls.Field.CACHE, cls.Field.SELF2CACHE])

    class Hideout:
        class Field:
            CACHE = "cache"

        @classmethod
        def get_or_lazyinit_cache(cls, hideout, v_lazy):
            if cls.Field.CACHE not in hideout:
                hideout[cls.Field.CACHE] = v_lazy()

            return hideout[cls.Field.CACHE]

        # @classmethod
        # def hideout2cache(cls, hideout):
        #     return hideout.get(cls.Field.CACHE)

        @classmethod
        def method2hideout(cls, owner, method):
            """
            owner needs to be passed because classmethod has no "__self__" before decorator
            """
            dict_method2hideout = AttributeTool.get_or_init(owner, CacheManager.Constant.ATTRIBUTE_NAME, {})
            hideout = DictTool.get_or_init(dict_method2hideout, FunctionTool.func2name(method), {})
            return hideout


    # def __init__(self, config, type):
    #     self.cache = cache
    #     self.key = key
    #     self.lock = lock

    @classmethod
    def add2cache(cls, callable_, v, args=None, kwargs=None,):
        config = cls.callable2config(callable_)
        key, lock = cls.Config.config2key(config), cls.Config.config2lock(config)

        cache = cls.callable2cache(callable_)

        k = key(*(args or []), **(kwargs or {}))
        CacheTool.cache_key2set(cache, k, v, lock=lock)

    # @classmethod
    # def object2h_manager(cls, object):
    #     v = AttributeTool.get_or_init(object, cls.Constant.ATTRIBUTE_NAME, {})
    #     assert_equal(getattr(object, cls.Constant.ATTRIBUTE_NAME), v)
    #     return v

    @classmethod
    def callable2config(cls, callable_):
        return getattr(callable_, cls.Constant.ATTRIBUTE_NAME, )


    @classmethod
    def callable2cache(cls, callable_):
        logger = FoxylibLogger.func_level2logger(cls.callable2cache, logging.DEBUG)

        callable_type = CallableTool.callable2type(callable_)
        logger.debug({"callable_type":callable_type})

        config = cls.callable2config(callable_)
        logger.debug({"config": config})

        if callable_type in {CallableTool.Type.FUNCTION, }:
            return cls.Config.config2cache(config)

        elif callable_type in {CallableTool.Type.INSTANCEMETHOD, CallableTool.Type.CLASSMETHOD}:
            owner = MethodTool.method2owner(callable_)
            hideout = cls.Hideout.method2hideout(owner, callable_)

            self2cache = cls.Config.config2self2cache(config)
            return cls.Hideout.get_or_lazyinit_cache(hideout, lambda: self2cache(owner))

        raise RuntimeError("Invalid callable type: {}".format(type(callable_)))

    # @classmethod
    # def func2manager(cls, func):
    #     return getattr(func, cls.Constant.ATTRIBUTE_NAME)


    # @classmethod
    # def attach2method(cls, func=None, self2cache=None, key=None, lock=None, ):
    #     logger = FoxylibLogger.func_level2logger(cls.attach2method, logging.DEBUG)
    #
    #     assert_is_not_none(self2cache)
    #     key = key or hashkey
    #
    #     def wrapper(f):
    #         @wraps(f)
    #         def wrapped(self, *_, **__):
    #             # make sure we get the same cache for same 'self'
    #             h_manager = cls.object2h_manager(self)
    #             manager_raw = {cls.Field.CACHE: self2cache(self),
    #                            cls.Field.KEY: key,
    #                            cls.Field.LOCK: lock,
    #                            }
    #
    #             method = MethodTool.owner_function2method(self, f)
    #             manager = DictTool.get_or_lazyinit(h_manager, method, lambda: manager_raw)
    #
    #             # logger.debug({"self": self, "f": f, "h_manager": h_manager, "manager": manager})
    #             # logger.debug({"cls.object2h_manager(self)":cls.object2h_manager(self)})
    #             return f(self, *_, **__)
    #
    #         return wrapped
    #
    #     return wrapper(func) if func else wrapper


    # @classmethod
    # def attach(cls, func=None, self2cache=None, cache=None, key=None, lock=None,):
    #     assert_not_equal(bool(cache), bool(self2cache))
    #
    #     def wrapper(f):
    #         config_raw = {cls.Config.Field.CACHE: cache,
    #                       cls.Config.Field.SELF2CACHE: self2cache,
    #                       cls.Config.Field.KEY: key,
    #                       cls.Config.Field.LOCK: lock,
    #                       }
    #         config = DictTool.filter(lambda k, v: v, config_raw)
    #         setattr(f, cls.Constant.ATTRIBUTE_NAME, config)
    #         return f
    #
    #     return wrapper(func) if func else wrapper

    # @classmethod
    # def function2config(cls, f):
    #     return getattr(f, cls.Constant.ATTRIBUTE_NAME,)

    # @classmethod
    # def method2manager(cls, method):
    #     logger = FoxylibLogger.func_level2logger(cls.method2manager, logging.DEBUG)
    #     h_manager = cls.object2h_manager(MethodTool.method2owner(method))
    #     if not h_manager:
    #         return None
    #
    #     return h_manager.get(method)

    @classmethod
    def attach_cached(cls, func=None, cached=None, cache=None, key=None, lock=None,):
        logger = FoxylibLogger.func_level2logger(cls.attach_cached, logging.DEBUG)

        assert_is_not_none(cache)
        cached = cached or cachetools.cached

        config = DictTool.filter(lambda k, v: v is not None,
                                 {cls.Config.Field.CACHE: cache,
                                  cls.Config.Field.KEY: key or hashkey,
                                  cls.Config.Field.LOCK: lock,
                                  })
        kwargs = cls.Config.config2kwargs(config)

        def wrapper(f):
            """
            CLASSMETHOD can used cached() too.
            But for simplicity of the system, CLASSMETHOD is forced to use cachedmethod
            """
            types_valid = {CallableTool.Type.FUNCTION, }
            assert_in(CallableTool.callable2type(f), types_valid,
                      "For instancemethod, use attach_cachedmethod() instead")

            assert_false(hasattr(f, cls.Constant.ATTRIBUTE_NAME))
            setattr(f, cls.Constant.ATTRIBUTE_NAME, config)


            f_cached = cached(cache, **kwargs)(f)
            return f_cached

        return wrapper(func) if func else wrapper

    @classmethod
    def attach_cachedmethod(cls, func=None, cachedmethod=None, self2cache=None, key=None, lock=None, ):
        assert_is_not_none(self2cache)

        cachedmethod = cachedmethod or cachetools.cachedmethod

        config = DictTool.filter(lambda k, v: v is not None,
                                 {cls.Config.Field.SELF2CACHE: self2cache,
                                  cls.Config.Field.KEY: key or hashkey,
                                  cls.Config.Field.LOCK: lock,
                                  })
        kwargs = cls.Config.config2kwargs(config)

        def wrapper(f):
            types_valid = {CallableTool.Type.INSTANCEMETHOD,CallableTool.Type.CLASSMETHOD_BEFORE_DECORATOR,}
            assert_in(CallableTool.callable2type(f), types_valid,
                      "For functions, use attach_cached() instead")

            assert_false(hasattr(f, cls.Constant.ATTRIBUTE_NAME))
            setattr(f, cls.Constant.ATTRIBUTE_NAME, config)

            self2cache = cls.Config.config2self2cache(config)

            @wraps(f)
            def wrapped(self, *_, **__):
                # config = cls.callable2config(f)
                # _self2cache = cls.Config.config2cache(config)

                # f.__self__ doesn't work here because classmethod() is not called yet
                hideout = cls.Hideout.method2hideout(self, f)
                cache = cls.Hideout.get_or_lazyinit_cache(hideout, lambda: self2cache(self))

                f_with_cache = cachedmethod(lambda x: cache, **kwargs)(f)
                return f_with_cache(self, *_, **__)

            return wrapped

        return wrapper(func) if func else wrapper

    # @classmethod
    # def cachedmethod2use_manager(cls, func=None, cachedmethod=None, method2manager=None):
    #     logger = FoxylibLogger.func_level2logger(cls.cachedmethod2use_manager, logging.DEBUG)
    #
    #     assert_is_not_none(cachedmethod)
    #     method2manager = method2manager if method2manager else cls.method2manager
    #
    #     def wrapper(f):
    #         @wraps(f)
    #         def wrapped(self, *_, **__):
    #             manager = method2manager(MethodTool.owner_function2method(self, f))
    #             cache, key, lock = cls.manager2cache(manager), cls.manager2key(manager), cls.manager2lock(manager)
    #             # logger.debug({"hex(id(cache))":hex(id(cache)), "manager":manager, })
    #
    #             f_with_cache = cachedmethod(lambda x: cache, key=key, lock=lock)(f)
    #             # logger.debug({"cls.object2h_manager(self)":cls.object2h_manager(self)})
    #             return f_with_cache(self, *_, **__)
    #
    #         return wrapped
    #
    #     return wrapper(func) if func else wrapper


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
