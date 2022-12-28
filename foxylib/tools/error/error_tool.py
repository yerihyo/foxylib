import logging
from functools import wraps, partial

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class ErrorTool:
    @classmethod
    def log_if_error(cls, func=None, func2logger=None, err2msg=None,):
        if err2msg is None:
            err2msg = lambda e: e #'Exception raised: {0}'.format(e)

        if func2logger is None:
            func2logger = partial(FoxylibLogger.func_level2logger,
                                  level=logging.ERROR)

        def wrapper(f):
            @wraps(f)
            def wrapped(*_, **__):
                logger = func2logger(f)

                try:
                    return f(*_, **__)
                except Exception as e:
                    logger.exception(err2msg(e))
                    raise

            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def default_if_error(cls, func=None, default=None, exception_tuple=(Exception,),):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                try:
                    return f(*args,**kwargs)
                except exception_tuple:
                    return default
            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def f_if_error(cls, func=None, f_error=None, ):
        def wrapper(f):
            @wraps(f)
            def wrapped(*_, **__):
                try:
                    return f(*_, **__)
                except:
                    f_error(*_, **__)
                    raise

            return wrapped

        return wrapper(func) if func else wrapper

    # @classmethod
    # def raise_if_warning(cls, func=None, level=None):
    #     assert_true(level)
    #
    #     def wrapper(f):
    #         @wraps(f)
    #         def wrapped(*_, **__):
    #             owner = MethodTool.method2is_classmethod(f)
    #             with cls.assertNoLog(owner, level):
    #                 return f(*_, **__)
    #
    #         return wrapped
    #
    #     return wrapper(func) if func else wrapper
    #
