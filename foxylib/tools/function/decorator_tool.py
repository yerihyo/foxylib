import logging
from functools import wraps, partial

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class DecoratorTool:
    @classmethod
    def decorator2conditioned(cls, decorator_in, cond_in):
        def decorator_out(f):
            cond = cond_in() if callable(cond_in) else cond_in
            if not cond:
                return f

            return decorator_in(f)
        return decorator_out

    @classmethod
    def override_result(cls, func=None, func_override=None, ):
        logger = FoxylibLogger.func_level2logger(cls.override_result, logging.DEBUG)

        if not func_override:
            raise ValueError({'func_override':func_override})

        def wrapper(f):
            @wraps(f)
            def wrapped(*_, **__):
                f(*_, **__)
                return func_override(*_, **__)

            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def wrapper2decorator(cls, wrapper_in, func=None):
        wrapper_out = FunctionTool.wrapper2wraps_applied(wrapper_in)
        return wrapper_out(func) if func else wrapper_out

    @classmethod
    def wrapper_postprocess(cls, func, func_postprocess=None):
        @wraps(func)
        def wrapped(*_, **__):
            return func_postprocess(func(*_, **__))
        return wrapped

    # @classmethod
    # def decorator_postprocess(cls, func=None, func_postprocess=None):
    #     if func_postprocess is None:
    #         raise ValueError({'func_postprocess':func_postprocess})
    #
    #     wrapper = partial(cls.wrapper_postprocess,
    #                       func_postprocess=func_postprocess)
    #     decorator = cls.wrapper2decorator(wrapper)
    #     return decorator(func) if func else decorator

