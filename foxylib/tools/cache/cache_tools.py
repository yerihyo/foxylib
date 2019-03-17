import os
from functools import wraps

from nose.tools import assert_is_not_none

from foxylib.tools.file.file_tools import FileToolkit


class CacheToolkit:
    @classmethod
    def cache2hashable(cls, cache, f_pair):
        f_serialize, f_deserialize = f_pair

        def wrapper(func):
            def deserialize_and_func(*args, **kwargs):
                _args = tuple([f_deserialize(arg) for arg in args])
                _kwargs = {k: f_deserialize(v) for k, v in six.viewitems(kwargs)}
                return func(*_args, **_kwargs)

            cached_func = cache(deserialize_and_func)

            @wraps(func)
            def wrapped(*args, **kwargs):
                _args = tuple([f_serialize(arg) for arg in args])
                _kwargs = {k: f_serialize(v) for k, v in kwargs.items()}
                return cached_func(*_args, **_kwargs)

            wrapped.cache_info = cached_func.cache_info
            wrapped.cache_clear = cached_func.cache_clear
            return wrapped

        return wrapper

    @classmethod
    def cache_utf82file(cls, func=None, filepath=None,):
        assert_is_not_none(filepath)

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if os.path.exists(filepath):
                    utf8_cached = FileToolkit.filepath2utf8(filepath)
                    return utf8_cached

                utf8 = f(*args,**kwargs)
                FileToolkit.utf82file(utf8, filepath)

                return utf8

            return wrapped

        return wrapper(func) if func else wrapper
