import inspect
import time
from datetime import datetime, timedelta
from functools import wraps, reduce, partial
from operator import itemgetter as ig
from typing import Any, Callable, TypeVar, Union

import pytz

from foxylib.tools.native.clazz.class_tool import ClassTool

T = TypeVar("T")

class FunctionTool:
    @classmethod
    def x2funced(cls, x, funcs):
        for f in funcs:
            f(x)
        return x

    @classmethod
    def bypass_none(cls, f_in):
        def f_out(x, *_, **__):
            if x is None:
                return None
            return f_in(x, *_, **__)
        return f_out

    @classmethod
    def bypass_false2none(cls, f_in):
        def f_out(x, *_, **__):
            if not x:
                return None
            return f_in(x, *_, **__)

        return f_out

    @classmethod
    def f2null_skipped(cls, f_in):
        def f_out(x):
            return f_in(x) if x is not None else x
        return f_out

    @classmethod
    def f_binary2f_nary(cls, f_binary, default=None):
        def f_nary(l):
            if not l:
                return default

            return reduce(f_binary, l[1:], l[0])
        return f_nary


    @classmethod
    def func2wrapped_delayed(cls, func, secs: Union[int, float]):
        @wraps(func)
        def wrapped(*_, **__):
            time.sleep(secs)
            return func(*_, **__)

        return wrapped

    @classmethod
    def func2wrapped_scheduled(cls, func: Callable[..., T], datetime_pivot: datetime):
        @wraps(func)
        def wrapped(*_, **__):
            dt_now = datetime.now(tz=pytz.utc)
            secs_sleep = (datetime_pivot - dt_now) / timedelta(seconds=1)
            if secs_sleep > 0:
                time.sleep(secs_sleep)
            return func(*_, **__)

        return wrapped

    @classmethod
    def sleep_and_repeat(cls, func, f_secs):
        while True:
            secs = f_secs()
            if secs is None:
                break

            time.sleep(secs)
            func()

    @classmethod
    def func2conditioned(cls, f, cond):
        def f_conditioned(x):
            if not cond(x):
                return x

            return f(x)

        return f_conditioned

    class Decorator:
        @classmethod
        def compare2ordering(cls, clazz):
            """
            Reference: functools.total_ordering
            :param clazz:
            :return:
            """
            def lt_from_compare(self, x):
                v = self.compare(x)
                if v is NotImplemented:
                    return v
                return v < 0

            def le_from_compare(self, x):
                v = self.compare(x)
                if v is NotImplemented:
                    return v
                return v <= 0

            def gt_from_compare(self, x):
                v = self.compare(x)
                if v is NotImplemented:
                    return v
                return v > 0

            def ge_from_compare(self, x):
                v = self.compare(x)
                if v is NotImplemented:
                    return v
                return v >= 0

            convert = [('__lt__', lt_from_compare),
                       ('__le__', le_from_compare),
                       ('__gt__', gt_from_compare),
                       ('__ge__', ge_from_compare),
                       ]

            """Class decorator that fills in missing ordering methods"""
            # Find user-defined comparisons (not those inherited from object).
            op_existing = {op for op in map(ig(0),convert) if getattr(clazz, op, None) is not getattr(object, op, None)}

            for opname, opfunc in convert:
                if opname not in op_existing:
                    opfunc.__name__ = opname
                    setattr(clazz, opname, opfunc)
            return clazz

    @classmethod
    def funcs_cond2compiled(cls, funcs, f_cond):
        def wrapped(x_in, *_, **__):
            for f in funcs:
                x_out = f(x_in, *_, **__)
                is_good = f_cond(x_out, x_in, *_, **__)
                if is_good:
                    return x_out

            return x_in
        return wrapped

    # @classmethod
    # def func2func_if_condition(cls, f, f_cond):
    #     def wrapped(x_in, *_, **__):
    #         x_out = f(x_in, *_, **__)
    #         is_good = f_cond(x_out, x_in, *_, **__)
    #         # print({'f':f, 'x_in':x_in, 'x_out':x_out, 'f_cond':f_cond, 'is_good':is_good})
    #         return x_out if is_good else x_in
    #     return wrapped

    @classmethod
    def func2name(cls, func):
        return func.__name__

    @classmethod
    def func2args_rshifted(cls, f_in, n):
        # @wraps(f_in)
        def f_out(*a, **__):
            return f_in(*a[n:], **__)
        return f_out

    @classmethod
    def xf2y(cls, x,f):
        return f(x)

    @classmethod
    def returnvalue2func_simple(cls, rv):
        return lambda: rv

    @classmethod
    def returnvalue2func(cls, rv):
        def f(*_,**__): return rv
        return f

    @classmethod
    def func2batch(cls, f):
        def f_batch(l):
            yield from map(f, l)

        return f_batch

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
    def func2class_func_name_list(cls, f):
        l = []

        clazz = FunctionTool.func2cls(f)
        if clazz: l.append(ClassTool.cls2name(clazz))
        l.append(FunctionTool.func2name(f))

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
    def args2split(cls, args, indexes_each):
        n = len(args)

        from foxylib.tools.collections.collections_tool import list2singleton
        p = list2singleton([len(args[index_each]) for index_each in indexes_each])

        def j2args_each(j):
            return [args[i] if i not in indexes_each else args[i][j]
                    for i in range(n)]

        args_list = [j2args_each(j) for j in range(p)]
        return args_list


    @classmethod
    def wrapper2wraps_applied(cls, wrapper_in):

        def func2wrapped(f):
            def wrapped(*_, **__): return f(*_, **__)
            return wrapped

        def wrapper(f):
            return wraps(f)(func2wrapped(wrapper_in(f)))

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

    @classmethod
    def partial_n_wraps(cls, f, *_, **__):
        return wraps(f)(partial(f, *_, **__))

    @classmethod
    def func2func_duration_prepended(cls, func):
        @wraps(func)
        def wrapped(*_, **__):
            time_start = time.time()
            result = func(*_, **__)
            time_end = time.time()
            exec_time = time_end - time_start

            return exec_time, result
        return wrapped

    @classmethod
    def func2process_prepended(cls, func, preprocess):
        @wraps(func)
        def wrapped(*_, **__):
            preprocess(*_, *__)
            return func(*_, **__)

        return wrapped

    @classmethod
    def func2postprocess_appended(cls, func, postprocess):
        @wraps(func)
        def wrapped(*_, **__):
            v1 = func(*_, **__)
            # logger.debug({'_': _, '__': __, 'v1': v1})
            v2 = postprocess(v1)
            return v2

        return wrapped

    @classmethod
    def func2tee(cls, func, f_tee):
        @wraps(func)
        def wrapped(*_, **__):
            v = func(*_, **__)
            # raise Exception(f_tee)

            f_tee(v)
            return v

        return wrapped

    @classmethod
    def func2functee(cls, func, f_functee):
        @wraps(func)
        def wrapped(*_, **__):
            v = func(*_, **__)
            # raise Exception(f_tee)

            f_functee(func, v)
            return v

        return wrapped

    @classmethod
    def wrapper2classed(cls, clazz2wrapper):
        def wrapper_out(func):
            @wraps(func)
            def wrapped(clazz, *_, **__):
                wrapper_raw = clazz2wrapper(clazz)
                f_wrapped = wrapper_raw(func)
                v = f_wrapped(clazz, *_, **__)
                return v
            return wrapped
        return wrapper_out



wrap2negate = FunctionTool.wrap2negate


f_a2t = FunctionTool.f_args2f_tuple
funcs2piped = FunctionTool.funcs2piped
idfun = FunctionTool.idfun

funcs2f_all = FunctionTool.funcs2f_all

rv2f0 = FunctionTool.returnvalue2func_simple
rv2f = FunctionTool.returnvalue2func
xf2y = FunctionTool.xf2y
partial_n_wraps = FunctionTool.partial_n_wraps