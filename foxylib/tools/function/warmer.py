import inspect
import logging

from foxylib.tools.collections.collections_tool import lchain

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.module.module_tool import ModuleTool


class Warmer:
    def __init__(self, module):
        super(Warmer, self).__init__()
        self.module = module
        self.h = {}

    @classmethod
    def _func2key(cls, f):
        return FunctionTool.func2module_qualname(f)

    def add(self, func=None, cond=True, args=None, kwargs=None,):
        logger = FoxylibLogger.func_level2logger(self.add, logging.DEBUG)
        # logger.debug({"cond": cond, "func":func})

        cls = self.__class__
        _args = args or []
        _kwargs = kwargs or {}

        def wrapper(f):
            if cond:
                k = cls._func2key(f)
                self.h[k] = (_args, _kwargs)

            return f

        return wrapper(func) if func else wrapper

    @classmethod
    def _dict2warmup(cls, h, target_list):
        logger = FoxylibLogger.func_level2logger(cls._dict2warmup, logging.DEBUG)
        # logger.debug({"h": h, })

        h_k2f = {}
        predicate = lambda x: any([inspect.ismethod(x),
                                   inspect.isfunction(x),
                                   ])
        for target in target_list:
            for name, f in inspect.getmembers(target, predicate=predicate):
                k = cls._func2key(f)
                h_k2f[k] = f

        # logger.debug({"target_list": target_list, "h_k2f": h_k2f, })

        for k, (args, kwargs) in h.items():
            logger.debug({"k":k, "f":f,})

            f = h_k2f[k]
            f(*args, **kwargs)

    def warmup(self, target_list=None, ):
        logger = FoxylibLogger.func_level2logger(self.warmup, logging.DEBUG)

        cls = self.__class__
        if target_list is None:
            target_list = lchain([self.module], ModuleTool.module2classes_within(self.module))

        cls._dict2warmup(self.h, target_list)
