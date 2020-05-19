import logging
from functools import wraps, lru_cache
from types import FunctionType, MethodType

import cachetools.keys
from future.utils import lfilter, lmap
from nose.tools import assert_is_not_none, assert_equal

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import AttributeTool
from foxylib.tools.string.string_tool import format_str


class CachetoolsToolDecorator:
    @classmethod
    def cached_each(cls, cache, index_each, key=cachetools.keys.hashkey, lock=None):
        logger = FoxylibLogger.func_level2logger(cls.cached_each, logging.DEBUG)

        """Decorator to wrap a function with a memoizing callable that saves
        results in a cache for each obj given a list of objects.

        Motivated by cachetools.cached
        """
        assert_is_not_none(cache)
        assert_is_not_none(index_each)

        def args_indexes2filtered(args_in, indexes):
            n = len(args_in)

            def i2arg(i):
                arg = args_in[i]
                if i != index_each:
                    return arg

                return lmap(lambda j: arg[j], indexes)

            args_out = [i2arg(i) for i in range(n)]
            return args_out

        def decorator(f_batch):
            def wrapper(*args, **__):
                # obj_list = list(objs)
                # n = len(obj_list)

                args_list = FunctionTool.args2split(args, index_each)
                k_list = [key(*args_each, **__) for args_each in args_list]
                n = len(k_list)

                def h_i2j_missing():
                    i_list_missing = lfilter(lambda i: k_list[i] not in cache, range(n))
                    return {i: j for j, i in enumerate(i_list_missing)}

                if lock is not None:
                    with lock:
                        h_i2j_missing = h_i2j_missing()
                else:
                    h_i2j_missing = h_i2j_missing()

                def run_f_batch(i_list_missing):
                    args_missing = args_indexes2filtered(args, i_list_missing)
                    v_list_missing = f_batch(*args_missing, **__)

                    # logger.debug({"len(i_list_missing)": len(i_list_missing),
                    #               "len(v_list_missing)": len(v_list_missing),
                    #               })

                    assert_equal(len(i_list_missing), len(v_list_missing),
                                 msg=format_str("f_batch result incorrect: {} vs {}",
                                                len(i_list_missing), len(v_list_missing)),
                                 )
                    return v_list_missing

                v_list_missing = run_f_batch(list(h_i2j_missing.keys())) if h_i2j_missing else []

                def v_iter():
                    for i,k in enumerate(k_list):

                        if i not in h_i2j_missing:
                            if lock is not None:
                                with lock:
                                    yield cache[k]
                            else:
                                yield cache[k]
                        else:
                            j = h_i2j_missing[i]
                            v = v_list_missing[j]

                            if lock is not None:
                                with lock:
                                    cache[k] = v
                            else:
                                cache[k] = v

                            yield v

                return list(v_iter())

            return cachetools._update_wrapper(wrapper, f_batch)

        return decorator

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

    def __init__(self, cache, key):
        self.cache = cache
        self.key = key

    def add2cache(self, obj, args=None, kwargs=None,):
        k = self.key(*(args or []), **(kwargs or {}))
        self.cache[k] = obj

    @classmethod
    def object2h_manager(cls, object):
        return AttributeTool.get_or_init(object, cls.Constant.ATTRIBUTE_NAME, {})

    @classmethod
    def callable2manager(cls, callable):
        logger = FoxylibLogger.func_level2logger(cls.callable2manager, logging.DEBUG)

        if isinstance(callable, FunctionType):
            return getattr(callable, cls.Constant.ATTRIBUTE_NAME)

        if isinstance(callable, MethodType):
            logger.debug({"callable.__self__": callable.__self__,
                          "callable": callable,
                          "callable.__name__": callable.__name__,
                          })

            h_manager = cls.object2h_manager(callable.__self__)
            if not h_manager:
                return None

            return h_manager.get(callable.__name__)


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
    def attach2method(cls, func=None, cachedmethod=None, self2cache=None, key=None, ):
        logger = FoxylibLogger.func_level2logger(cls.attach2method, logging.DEBUG)

        assert_is_not_none(self2cache)
        cachedmethod = cachedmethod if cachedmethod else cachetools.cachedmethod
        key = key if key else cachetools.keys.hashkey

        def wrapper(f):
            @wraps(f)
            def wrapped(self, *_, **__):
                # make sure we get the same cache for same 'self'
                h_manager = cls.object2h_manager(self)
                manager = DictTool.get_or_init_lazy(h_manager, f.__name__, lambda: cls(self2cache(self), key,))

                logger.debug({"self":self, "f":f, "h_manager": h_manager,})
                f_with_cache = cachedmethod(lambda x: manager.cache, key=key)(f)
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

