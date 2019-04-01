import inspect
from functools import wraps, reduce

from foxylib.tools.native.class_tools import ClassToolkit, ModuleToolkit


class FunctionToolkit:
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
        def wrapped(*a, **k): return f(*a, **k)
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

wrap2negate = FunctionToolkit.wrap2negate

class Warmer:
    def __init__(self, module):
        super(Warmer, self).__init__()
        self.module = module
        self.h = {}

    @classmethod
    def _func2key(cls, f):
        return tuple([getattr(f, k) for k in ["__module__", "__qualname__"]])

    def add(self, func=None, cond=True, args=None, kwargs=None,):
        cls = self.__class__
        _args = args or []
        _kwargs = kwargs or {}

        def wrapper(f):
            if cond:
                k = cls._func2key(f)
                self.h[k] = (_args, _kwargs)

            return f

        if func:
            return wrapper(func)

        return wrapper

    @classmethod
    def _dict2warmup(cls, h, target_list):
        h_k2f = {}
        predicate = lambda x: any([inspect.ismethod(x),
                                   inspect.isfunction(x),
                                   ])
        for target in target_list:
            for name, f in inspect.getmembers(target, predicate=predicate):
                k = cls._func2key(f)
                h_k2f[k] = f

        for k, (args,kwargs) in h.items():
            f = h_k2f[k]
            f(*args, **kwargs)

    def warmup(self, target_list=None,):
        cls = self.__class__
        if target_list is None:
            target_list = [self.module] + ModuleToolkit.module2class_list(self.module)

        cls._dict2warmup(self.h, target_list)

f_a2t = FunctionToolkit.f_args2f_tuple
