import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from foxylib.tools.log.logger_tool import LoggerTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

logger = logging.getLogger(__name__)

class ThreadTool:
    @classmethod
    def func2threaded(cls, func=None, max_workers=None, ):
        logger = FoxylibLogger.func2logger(cls.func2threaded)

        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                executor = ThreadPoolExecutor(max_workers=max_workers)  # non-blocking

                def f_new(*args, **kwargs):
                    rv = f(*args, **kwargs)

                    logger.info({"message": "func2thread", "value": rv})
                    LoggerTool.logger2flush_handlers(logger)

                    return rv

                future = executor.submit(f_new, *args, **kwargs)
                # future.add_done_callback(lambda x: rs.setex(name, time, x.result()))
                return future

            return wrapped

        return wrapper(func) if func else wrapper

    @classmethod
    def future2result_or_raise(cls, future):
        exc_future = future.exception()
        if exc_future:
            logger.error({"messsage":"future2result_or_raise", "exception":exc_future})
            raise exc_future

        return future.result()
