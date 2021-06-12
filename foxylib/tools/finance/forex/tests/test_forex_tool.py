import logging
from decimal import Decimal
from pprint import pprint
from unittest import TestCase

import pytest

from foxylib.tools.finance.forex.forex_tool import ForexTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestForexTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='not serviced anymore?')
    def test_01(self):
        krw = Decimal(10000)
        hyp = ForexTool.cr().convert("KRW", "USD", krw)
        self.assertEqual(type(hyp), Decimal)

        self.assertLess(hyp, krw / 500)
        self.assertGreater(hyp, krw / 3000)

