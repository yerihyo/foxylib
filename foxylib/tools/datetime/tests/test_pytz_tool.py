from datetime import datetime
import logging
from unittest import TestCase

import pytz

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestPytzTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        # https://stackoverflow.com/a/27592919
        tz_seoul = pytz.timezone("Asia/Seoul")

        if False:
            """ true most of the time, but lets avoid unnecessary unittest error"""
            self.assertEqual(datetime.now(tz_seoul).strftime("%H:%M"),
                             datetime.now(pytz.utc).astimezone(tz_seoul).strftime("%H:%M"),
                             )

        dt_now_utc = datetime.now(pytz.utc)
        self.assertNotEqual(dt_now_utc.replace(tzinfo=tz_seoul),  # not necessarily UTC
                            dt_now_utc.astimezone(tz_seoul),
                            )

        tz_seoul = pytz.timezone("Asia/Seoul")
        dt_now_tz = dt_now_utc.astimezone(tz_seoul)
        self.assertEqual(datetime.combine(dt_now_tz.date(), dt_now_tz.time(), dt_now_tz.tzinfo),  # already UTC
                         dt_now_tz,
                         )

        self.assertNotEqual(datetime.combine(dt_now_tz.date(), dt_now_tz.time(), tz_seoul),  # not necessarily UTC
                            dt_now_tz,
                            )
