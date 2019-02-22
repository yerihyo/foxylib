import logging
from datetime import datetime
from functools import wraps

from foxylib.tools.native.class_tools import ClassToolkit
from foxylib.tools.native.function_tools import FunctionToolkit


class LoggerToolkit:
    @classmethod
    def level2str(cls, level):
        if level == logging.CRITICAL: return "critical"
        if level == logging.ERROR: return "error"
        if level == logging.WARNING: return "warning"
        if level == logging.INFO: return "info"
        if level == logging.DEBUG: return "debug"
        if level == logging.NOTSET: return "notset"
        raise Exception()

    # @classmethod
    # def add_handlers_and_return(cls, logger, handlers):
    #     for handler in handlers:
    #         logger.addHandler(handler)
    #     return logger

    @classmethod
    def func2name(cls, f):
        # filepath = inspect.getfile(f)
        # basename = os.path.splitext(os.path.basename(filepath))[0]
        l = [] #basename]

        clazz = FunctionToolkit.func2cls(f)
        if clazz: l.append(ClassToolkit.cls2name(clazz))
        l.append(FunctionToolkit.func2name(f))

        name = ".".join(l)
        return name

    @classmethod
    def logger2flush_handlers(cls, logger):
        for h in logger.handlers:
            h.flush()
            
    @classmethod
    def add_or_skip_handlers(cls, logger, handlers):
        if not handlers: return

        for handler in (handlers or []):
            if handler in logger.handlers: continue

            logger.addHandler(handler)

    @classmethod
    def kwargs2logger(cls, logger, handlers=None, level=None,):
        if handlers:
            cls.add_or_skip_handlers(logger, handlers)

        if level is not None:
            logger.setLevel(level)

        return logger

    @classmethod
    def func2logger(cls, func,):
        name = cls.func2name(func)
        logger = logging.getLogger(name)
        return logger

    @classmethod
    def func2init_logger(cls, func=None, func2logger=None,):
        def wrapper(f):
            _logger = None
            _func2logger = func2logger if func2logger else cls.func2logger
            @wraps(f)
            def wrapped(*args, **kwargs):
                nonlocal _logger
                if _logger is None:
                    _logger = _func2logger(f)

                result = f(*args, **kwargs)
                return result

            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def log_exec_duration(cls, func=None, msg=None, logger=None, ):
        def wrapper(f):
            _logger = logger
            _msg = msg

            @wraps(f)
            def wrapped(*args, **kwargs):
                nonlocal _logger
                if _logger is None:
                    _logger = cls.func2logger(f)

                nonlocal _msg
                if _msg is None:
                    _msg = "[{0}] exec time".format(FunctionToolkit.func2name(f))

                dt_start = datetime.now()
                result = f(*args, **kwargs)
                td_exec = datetime.now() - dt_start

                _logger.info({
                    'message': _msg,
                    'exec_ms': round(td_exec.total_seconds() * 1000, 3),
                })
                return result

            return wrapped

        return wrapper(func) if func else wrapper






