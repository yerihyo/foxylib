import inspect
import logging
import time
from functools import wraps, reduce

from future.utils import lfilter
from nose.tools import assert_equal

from foxylib.tools.native.class_tools import ClassToolkit


class FunctionToolkit:
    @classmethod
    def returnvalue2func_simple(cls, rv):
        return lambda: rv

    @classmethod
    def returnvalue2func(cls, rv):
        def f(*_,**__): return rv
        return f


    @classmethod
    def func2cls(cls, meth):
        if inspect.ismethod(meth):
            for clazz in inspect.getmro(meth.__self__.__class__):
                if clazz.__dict__.get(meth.__name__) is meth:
                    return clazz
            meth = meth.__func__  # fallback to __qualname__ parsing

        if inspect.isfunction(meth):
            str_path = meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
            clazz = reduce(getattr, str_path.split('.'), inspect.getmodule(meth),)
            if isinstance(clazz, type):
                return clazz
        return None

    @classmethod
    def func2name(cls, f): return f.__name__

    @classmethod
    def func2class_func_name_list(cls, f):
        l = []

        clazz = FunctionToolkit.func2cls(f)
        if clazz: l.append(ClassToolkit.cls2name(clazz))
        l.append(FunctionToolkit.func2name(f))

        return l

    @classmethod
    def func2class_func_name(cls, f):
        return ".".join(cls.func2class_func_name_list(f))

    @classmethod
    def wrap2negate(cls, f):
        def wrapped(*a, **k):
            return not f(*a, **k)
        return wrapped

    @classmethod
    def func2wrapped(cls, f):
        def wrapped(*_, **__): return f(*_, **__)
        return wrapped

    @classmethod
    def wrapper2wraps_applied(cls, wrapper_in):
        def wrapper(f):
            return wraps(f)(cls.func2wrapped(wrapper_in(f)))

        return wrapper

    @classmethod
    def f_args2f_tuple(cls, f_args):
        def f_tuple(args, **kwargs):
            return f_args(*args, **kwargs)

        return f_tuple

    @classmethod
    def funcs2piped(cls, funcs):
        if not funcs: raise Exception()

        def f(*args, **kwargs):
            v_init = funcs[0](*args, **kwargs)
            v = reduce(lambda x, f: f(x), funcs[1:], v_init)
            return v

        return f

    @classmethod
    def funcs2f_all(cls, f_list):
        def f_all(*_, **__):
            return all(f(*_,**__) for f in f_list)
        return f_all

    @classmethod
    def funcs2any(cls, f_list):
        def f_any(*_, **__):
            return all(f(*_, **__) for f in f_list)
        return f_any

    @classmethod
    def idfun(cls, x):
        return x


    @classmethod
    def func2module_qualname(cls, f):
        return tuple([getattr(f, k) for k in ["__module__", "__qualname__"]])

    @classmethod
    def func2fullpath(cls, f):
        return ".".join(cls.func2module_qualname(f))



wrap2negate = FunctionToolkit.wrap2negate


f_a2t = FunctionToolkit.f_args2f_tuple
funcs2piped = FunctionToolkit.funcs2piped
idfun = FunctionToolkit.idfun

funcs2f_all = FunctionToolkit.funcs2f_all

rv2f0 = FunctionToolkit.returnvalue2func_simple
rv2f = FunctionToolkit.returnvalue2func