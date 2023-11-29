import logging
import math
from datetime import datetime, timedelta, time
from unittest import TestCase

import dateutil.parser
import pytz

from foxylib.tools.datetime.datetime_tool import DatetimeTool, DatetimeUnit, \
    TimedeltaTool, TimeTool, Nearest
from foxylib.tools.datetime.pytz_tool import PytzTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        self.assertEqual(
            dateutil.parser.parse('20221028094822'),
            datetime(2022, 10, 28, 9, 48, 22),
        )

    def test_2(self):
        self.assertNotEqual(
            pytz.timezone('Asia/Seoul').localize(dateutil.parser.parse('20221028094822')),
            datetime(2022, 10, 28, 9, 48, 22),
        )

    def test_3(self):
        print(pytz.timezone('Asia/Seoul').localize(dateutil.parser.parse('20221028094822')).strftime('%Y%m%d_%H%M%S'))

        # print(DatetimeTool.now_utc().isoformat())
        # print(datetime.now().strftime('%Y%m%d_%H%M%S'))
        # print(dateutil.parser.parse('20221028094822').isoformat())



class TestDatetimeTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        tz_la = pytz.timezone("America/Los_Angeles")

        dt_from = datetime(2020, 1, 1, tzinfo=tz_la)
        dt_to = datetime(2020, 1, 2, tzinfo=tz_la)

        hyp = DatetimeTool.datetime_pair2days_difference((dt_from, dt_to,))
        self.assertEqual(hyp, 1)


    # daylight saving start
    def test_02(self):

        tz_la = pytz.timezone("America/Los_Angeles")

        dt_from = datetime(2020, 3, 7, tzinfo=tz_la)
        dt_to = datetime(2020, 3, 9, tzinfo=tz_la)

        hyp = DatetimeTool.datetime_pair2days_difference((dt_from, dt_to,))
        self.assertEqual(hyp, 2)

    # daylight saving end
    def test_03(self):
        tz_la = pytz.timezone("America/Los_Angeles")

        dt_from = datetime(2020, 10, 31, tzinfo=tz_la)
        dt_to = datetime(2020, 11, 2, tzinfo=tz_la)

        hyp = DatetimeTool.datetime_pair2days_difference((dt_from, dt_to,))
        self.assertEqual(hyp, 2)

    def test_04(self):
        dt_pivot = datetime(2022, 2, 2, 22, 22, 22, 222222)

        hyp = DatetimeTool.floor(dt_pivot, DatetimeUnit.MILLISECOND,)
        ref = datetime(2022, 2, 2, 22, 22, 22, 222000)
        self.assertEqual(hyp, ref)

    def test_05(self):
        dt_start = datetime(2020, 2, 29, 22, 22, 22, 222222)
        dt_end = datetime(2021, 2, 28, 22, 22, 22, 222222)

        hyp = DatetimeTool.datetime_span2years([dt_start,dt_end])
        ref = 0
        self.assertEqual(hyp, ref)

    def test_06(self):
        dt_start = datetime(2020, 2, 28, 22, 22, 22, 222222)
        dt_end = datetime(2021, 2, 28, 22, 22, 22, 222222)

        hyp = DatetimeTool.datetime_span2years([dt_start,dt_end])
        ref = 1
        self.assertEqual(hyp, ref)

    def test_07(self):
        td = timedelta(days=7, seconds=4*60*60+7*60+5, microseconds=2312)

        unit_day = TimedeltaTool.unit_day()
        unit_hour = TimedeltaTool.unit_hour()
        unit_minute = TimedeltaTool.unit_minute()
        unit_second = TimedeltaTool.unit_second()

        self.assertEqual(TimedeltaTool.timedelta_unit_pair2quotient(td, unit_hour, unit_day), 4)
        self.assertEqual(TimedeltaTool.timedelta_unit_pair2quotient(td, unit_minute, unit_hour), 7)
        self.assertEqual(TimedeltaTool.timedelta_unit_pair2quotient(td, unit_second, unit_minute), 5)

    def test_08(self):
        tz = pytz.timezone("Asia/Seoul")
        dt = DatetimeTool.astimezone(datetime.now(pytz.utc), tz)
        dt_truncate = DatetimeTool.truncate(dt, DatetimeUnit.SECOND)

        self.assertEqual(dt.year, dt_truncate.year)
        self.assertEqual(dt.month, dt_truncate.month)
        self.assertEqual(dt.day, dt_truncate.day)
        self.assertEqual(dt.hour, dt_truncate.hour)
        self.assertEqual(dt.minute, dt_truncate.minute)
        if dt.second:
            self.assertNotEqual(dt.second, dt_truncate.second)

        if dt.microsecond:
            self.assertNotEqual(dt.microsecond, dt_truncate.microsecond)

    def test_09(self):
        tz = pytz.timezone("Asia/Seoul")

        dt_pivot = datetime(2020, 1, 1, 5, 15, 31, tzinfo=pytz.utc)

        dt_01 = DatetimeTool.datetime2nearest(dt_pivot,
                                              datetime(2020, 1, 1, 5, tzinfo=pytz.utc),
                                              timedelta(minutes=2),
                                              Nearest.PAST,
                                              )
        self.assertEqual(dt_01, datetime(2020, 1, 1, 5, 14, tzinfo=pytz.utc))

        dt_02 = DatetimeTool.datetime2nearest(dt_pivot,
                                              datetime(2020, 1, 1, 5, tzinfo=pytz.utc),
                                              timedelta(minutes=2),
                                              Nearest.COMING,
                                              )
        self.assertEqual(dt_02, datetime(2020, 1, 1, 5, 16, tzinfo=pytz.utc))


class TestTimeTool(TestCase):
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        tz = pytz.timezone("America/Los_Angeles")
        dt_tz = datetime.now(tz=tz)

        hours_1 = timedelta(seconds=60 * 60)
        hours_23 = timedelta(seconds=60 * 60 * 23)
        hours_24 = timedelta(seconds=60 * 60 * 24)
        # hours_25 = timedelta(seconds=60 * 60 * 25)

        time_past = (dt_tz - timedelta(seconds=60 * 5)).timetz()
        dt_coming_of_past = TimeTool.time2datetime_nearest(dt_tz, time_past, timedelta(days=1), Nearest.COMING)

        self.assertGreater(dt_coming_of_past, dt_tz + hours_23)
        self.assertLess(dt_coming_of_past, dt_tz + hours_24)

        time_future = (dt_tz + timedelta(seconds=60 * 5)).timetz()

        dt_coming_of_future = TimeTool.time2datetime_nearest(dt_tz, time_future, timedelta(days=1), Nearest.COMING)

        self.assertGreater(dt_coming_of_future, dt_tz)
        # raise Exception({"dt_tz + hours_24": dt_tz + hours_24,
        #                  "dt_future_of_future": dt_future_of_future,
        #                  })

        self.assertLess(dt_coming_of_future, dt_tz + hours_1)

    def test_02(self):
        dt_now = datetime.now(pytz.utc)
        dt_from = dt_now - timedelta(seconds=60)
        dt_result = DatetimeTool.from_pivot_period2next(dt_from, dt_now, timedelta(days=1))

        self.assertEqual(dt_result, dt_from + timedelta(days=1))

    def test_03(self):
        td = timedelta(days=1, seconds=2)
        self.assertEqual(math.ceil(td / timedelta(days=1)), 2)


class TestTimedeltaTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(TimedeltaTool.rune2timedelta("1m30s"),
                         timedelta(minutes=1, seconds=30))

        self.assertEqual(TimedeltaTool.rune2timedelta("2w 30s"),
                         timedelta(weeks=2, seconds=30))

        self.assertEqual(TimedeltaTool.rune2timedelta("- 3d 90m"),
                         -timedelta(days=3, hours=1, minutes=30))

    def test_02(self):
        self.assertEqual(
            TimedeltaTool.timedelta2rune(timedelta(minutes=1, seconds=30)),
            "1m 30s",
        )

        self.assertEqual(
            TimedeltaTool.timedelta2rune(timedelta(weeks=2, seconds=30)),
            "14d 30s",
        )

        self.assertEqual(
            TimedeltaTool.timedelta2rune(-timedelta(days=3, hours=1, minutes=30)),
            "- 3d 1h 30m",
        )
