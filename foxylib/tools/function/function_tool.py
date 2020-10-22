import inspect
from functools import wraps, reduce, partial, total_ordering
from operator import itemgetter as ig

from foxylib.tools.native.clazz.class_tool import ClassTool


class FunctionTool:

    @classmethod
    def func2percolative(cls, f):
        def f_percolative(x):
            if isinstance(x, dict):
                return {k:f_percolative(v) for k,v in x.items()}

            if isinstance(x, (list,tuple,set)):
                return type(x)(map(f_percolative, x))

            return f(x)
        return f_percolative


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
    def func2func_if_condition(cls, f, f_cond):
        def wrapped(x_in, *_, **__):
            x_out = f(x_in, *_, **__)
            is_good = f_cond(x_out, x_in, *_, **__)
            # print({'f':f, 'x_in':x_in, 'x_out':x_out, 'f_cond':f_cond, 'is_good':is_good})
            return x_out if is_good else x_in
        return wrapped

    @classmethod
    def func2name(cls, func):
        return func.__name__

    @classmethod
    def shift_args(cls, f_in, n):
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



wrap2negate = FunctionTool.wrap2negate


f_a2t = FunctionTool.f_args2f_tuple
funcs2piped = FunctionTool.funcs2piped
idfun = FunctionTool.idfun

funcs2f_all = FunctionTool.funcs2f_all

rv2f0 = FunctionTool.returnvalue2func_simple
rv2f = FunctionTool.returnvalue2func
xf2y = FunctionTool.xf2y
partial_n_wraps = FunctionTool.partial_n_wraps