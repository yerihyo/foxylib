import inspect




class FunctionToolkit:
    @classmethod
    def func2cls(cls, meth):
        if inspect.ismethod(meth):
            for cls in inspect.getmro(meth.__self__.__class__):
                if cls.__dict__.get(meth.__name__) is meth:
                    return cls
            meth = meth.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(meth):
            cls = getattr(inspect.getmodule(meth),
                          meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
        return None

    @classmethod
    def func2name(cls, f): return f.__name__

    @classmethod
    def negate(cls, f):
        def f_negated(*args, **kwargs):
            return not f(*args,**kwargs)
        return f_negated


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
