from functools import wraps

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class ErrorTool:
    @classmethod
    def log_when_error(cls, func=None, logger=None, err2msg=None,):
        if err2msg is None:
            err2msg = lambda e: e #'Exception raised: {0}'.format(e)

        def wrapper(f):
            @wraps(f)
            def wrapped(*_, **__):
                _logger = logger if logger else FoxylibLogger.func2logger(f)

                try:
                    return f(*_, **__)
                except Exception as e:
                    _logger.exception(err2msg(e))
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
