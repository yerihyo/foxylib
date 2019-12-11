import logging
from unittest import TestCase

from dateutil import relativedelta

from foxylib.tools.date.date_tools import RelativeDeltaToolkit


class RelativeDeltaToolkitTest(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_success_01(self):
        hyp = RelativeDeltaToolkit.parse_str2reldelta("+3일")
        ref = relativedelta.relativedelta(days=3)
        self.assertEqual(hyp, ref)

    def test_success_02(self):
        hyp = RelativeDeltaToolkit.parse_str2reldelta("+20 초")
        ref = relativedelta.relativedelta(seconds=20)
        self.assertEqual(hyp, ref)

    def test_success_03(self):
        hyp = RelativeDeltaToolkit.parse_str2reldelta("-1개월 6일")
        ref = relativedelta.relativedelta(months=-1, days=-6,)
        self.assertEqual(hyp, ref)

    def test_success_04(self):
        hyp = RelativeDeltaToolkit.parse_str2reldelta("- 10 mins")
        ref = relativedelta.relativedelta(minutes=-10,)
        self.assertEqual(hyp, ref)
