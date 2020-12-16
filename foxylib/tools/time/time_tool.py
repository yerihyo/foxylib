import logging
import time
from datetime import datetime

import pytz

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TimeTool:
    @classmethod
    def secs2sleep(cls, secs):
        logger = FoxylibLogger.func_level2logger(cls.secs2sleep, logging.DEBUG)

        logger.debug("sleeping {:.2f} secs".format(secs))
        time.sleep(secs)

    @classmethod
    def sleep_until(cls, dt_until):
        from foxylib.tools.datetime.datetime_tool import DatetimeTool
        from foxylib.tools.datetime.datetime_tool import TimedeltaTool

        logger = FoxylibLogger.func_level2logger(cls.sleep_until, logging.DEBUG)

        tz = pytz.utc if DatetimeTool.dt2is_aware(dt_until) else None
        dt_now = datetime.now(tz=tz)
        td = dt_now - dt_until

        if td >= 0:
            secs = TimedeltaTool.td2secs(td)

            logger.debug("sleeping until {}".format(dt_until.isoformat()))
            time.sleep(secs)
