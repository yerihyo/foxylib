from functools import wraps

import cachetools.keys
from future.utils import lfilter, lmap
from nose.tools import assert_is_not_none

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.function.function_tool import FunctionTool


class CachetoolsToolDecorator:
    @classmethod
    def cached_each(cls, cache, index_each, key=cachetools.keys.hashkey, lock=None):
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

                args_missing = args_indexes2filtered(args, h_i2j_missing.keys())
                v_list_missing = f_batch(*args_missing, **__)

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
    def __init__(self, cache, key):
        self.cache = cache
        self.key = key

    def add2cache(self, obj, args=None, kwargs=None,):
        k = self.key(*(args or []), **(kwargs or {}))
        self.cache[k] = obj

    @classmethod
    def attach2func(cls, func=None, cached=None, cache=None, key=None,):
        assert_is_not_none(cache)

        if cached is None:
            cached = cachetools.cached

        if key is None:
            key = cachetools.keys.hashkey

        cachetools_manager = cls(cache, key,)

        def wrapper(f):
            f.cachetools_manager = cachetools_manager
            return cached(cache, key=key,)(f)

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

