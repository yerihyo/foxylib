from datetime import datetime
from datetime import datetime
from unittest import TestCase

import pytz

from foxylib.tools.date.date_tools import DatetimeTool, DatetimeUnit


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
