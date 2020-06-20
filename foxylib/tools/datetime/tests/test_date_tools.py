from datetime import datetime, timedelta
from datetime import datetime
from unittest import TestCase

import pytz

from foxylib.tools.datetime.datetime_tool import DatetimeTool, DatetimeUnit, TimedeltaTool


class DatetimeToolTest(TestCase):
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

        hyp = DatetimeTool.truncate(dt_pivot, unit=DatetimeUnit.Value.MILLISEC)
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
