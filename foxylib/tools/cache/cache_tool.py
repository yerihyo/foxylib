import logging
from functools import wraps, lru_cache

import cachetools
import dill
import six
from frozendict import frozendict
from future.utils import lmap
from nose.tools import assert_is_not_none, assert_equal, assert_true

from foxylib.tools.collections.collections_tool import zip_strict, list2singleton
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


# class CacheToolDecorator:
#     @classmethod
#     def cache_each(cls, func=None, cache=None):
#         def wrapper(f):
#             @wraps(f)
#             def wrapped(keys, *_, **__):
#                 key_list = list(keys)
#                 result_list = list(f(keys, *_, **__))
#
#                 # for key, result in izip_strict(list(key_list, result_list)
#                 return result_list
#
#             return wrapped
#
#         return wrapper(func) if func else wrapper
#
from foxylib.tools.string.string_tool import format_str


class CacheTool:
    # Decorator = CacheToolDecorator

    @classmethod
    @lru_cache(maxsize=1)
    def func_pair_identical(cls):
        def idfun(x):
            return x
        return idfun, idfun

    class JSON:
        @classmethod
        def func_pair(cls):
            return cls.serialize, cls.deserialize

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
                _args = tuple([f_deserialize(arg) for arg in args])
                _kwargs = {k: f_deserialize(v) for k, v in six.viewitems(kwargs)}

                # logger.debug({"func": func, "args": args, "_args": _args, "kwargs": kwargs, "_kwargs": _kwargs, })
                return func(*_args, **_kwargs)

            cached_func = cache(deserialize_and_func)

            @wraps(func)
            def wrapped(*args, **kwargs):
                # logger.debug({"func": func, "args": args, "kwargs": kwargs, })

                _args = tuple([f_serialize(arg) for arg in args])
                _kwargs = {k: f_serialize(v) for k, v in kwargs.items()}
                return cached_func(*_args, **_kwargs)

            if hasattr(cache, "cache_info"):
                wrapped.cache_info = cached_func.cache_info

            if hasattr(wrapped, "cache_clear"):
                wrapped.cache_clear = cached_func.cache_clear

            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def reader2get(cls, cache, reader, *_, lock=None, **__):

        if lock is not None:
            with lock:
                return reader(cache, *_, **__)
        else:
            return reader(cache, *_, **__)

    @classmethod
    def writer2set(cls, cache, writer, value, *_, lock=None, **__):
        if lock is not None:
            with lock:
                return writer(cache, value, *_, **__)
        else:
            return writer(cache, value, *_, **__)

    # @classmethod
    # def key2reader_default(cls, key):
    #     def reader(cache, *_, **__):
    #         k = key(*_, **__)
    #         return cache[k]
    #
    #     return reader


    @classmethod
    def k2get(cls, cache, k, lock=None):
        if lock is not None:
            with lock:
                return cache[k]
        else:
            return cache[k]

    # @classmethod
    # def key2writer_default(cls, key):
    #     def writer(cache, value, *_, **__):
    #         # raise Exception({"key":key})
    #         k = key(*_, **__)
    #         cache[k] = value
    #
    #     return writer
    #
    # @classmethod
    # def key2set(cls, cache, key, value, lock=None):
    #     return cls.writer2set(cache, cls.key2writer_default(key), value, lock=lock)

    @classmethod
    def k2set(cls, cache, k, value, lock=None):
        if lock is not None:
            with lock:
                cache[k] = value
        else:
            cache[k] = value
        return value

    @classmethod
    def delete_key(cls, cache, key, lock=None):
        def delete_if_exists(cache, key):
            if key in cache:
                del cache[key]

        if lock is not None:
            with lock:
                delete_if_exists(cache,key)
        else:
            delete_if_exists(cache, key)

    @classmethod
    def cache_keys2i_list_missing(cls, cache, k_list, lock=None):
        if lock is not None:
            with lock:
                i_list_missing = [i for i, k in enumerate(k_list) if k not in cache]
        else:
            i_list_missing = [i for i, k in enumerate(k_list) if k not in cache]

        return i_list_missing


class CacheBatchTool:



    @classmethod
    def batchrun_missing(cls, f_batch, args, kwargs, cache, indexes_each, k_list, lock=None):
        i_list_missing = CacheTool.cache_keys2i_list_missing(cache, k_list, lock=lock)
        if not i_list_missing:
            return {}

        def _indexes2args_filtered(indexes):
            def j2arg(j):
                arg = args[j]
                if j not in indexes_each:
                    return arg

                return lmap(lambda i: arg[i], indexes)

            args_out = [j2arg(j) for j in range(len(args))]
            return args_out

        args_missing = _indexes2args_filtered(i_list_missing, )
        v_list_missing = f_batch(*args_missing, **kwargs)

        assert_equal(len(i_list_missing), len(v_list_missing),
                     msg=format_str("f_batch result incorrect: {} vs {}",
                                    len(i_list_missing), len(v_list_missing)),
                     )

        h_i2v = dict(zip_strict(i_list_missing, v_list_missing))

        # raise Exception({"i_list_missing":i_list_missing,"v_list_missing":v_list_missing})
        return h_i2v

    @classmethod
    def batchrun(cls, f_batch, args, kwargs, cache, indexes_each, key, lock=None):
        logger = FoxylibLogger.func_level2logger(cls.batchrun, logging.DEBUG)
        # key = key if key else cachetools.keys.hashkey

        def args_kwargs2k_list(_key, _indexes_each, _args, _kwargs):
            _args_list = FunctionTool.args2split(_args, _indexes_each)
            return [key(*_args_each, **_kwargs) for _args_each in _args_list]

        k_list = args_kwargs2k_list(key, indexes_each, args, kwargs)
        n = len(k_list)

        h_i2v_missing = cls.batchrun_missing(f_batch, args, kwargs, cache, indexes_each, k_list, lock=lock)

        def index2value(index):
            # raise Exception({"index": index, "k_list":k_list, "h_i2v_missing": h_i2v_missing})

            k = k_list[index]
            if index not in h_i2v_missing:
                return CacheTool.k2get(cache, k, lock=lock)
            else:
                v = h_i2v_missing[index]
                CacheTool.k2set(cache, k, v, lock=lock)
                return v

        v_list = lmap(index2value, range(n))

        # logger.debug({"hex(id(cache))":hex(id(cache)), "cache":cache, "h_i2v_missing":h_i2v_missing})
        # raise Exception({"h_i2v_missing":h_i2v_missing,"v_list":v_list})

        return v_list


class Timedvalue:
    class Field:
        UPDATED_AT = "updated_at"
        VALUE = "value"

    @classmethod
    def timedvalue2updated_at(cls, timedvalue):
        return timedvalue.get(cls.Field.UPDATED_AT)

    @classmethod
    def timedvalue2value(cls, timedvalue):
        return timedvalue.get(cls.Field.VALUE)

    @classmethod
    def timedvalue2is_outdated(cls, timedvalue, dt_pivot):
        assert_true(dt_pivot)

        if not timedvalue:
            return True

        updated_at = cls.timedvalue2updated_at(timedvalue)
        if not updated_at:
            return True

        return dt_pivot > updated_at

    # @classmethod
    # def timedvalue_datetime2value(cls, timedvalue, dt_pivot):
    #     if cls.timedvalue2is_outdated(timedvalue, dt_pivot):
    #         return None
    #
    #     assert(cls.Field.VALUE in timedvalue)
    #     return timedvalue[cls.Field.VALUE]


