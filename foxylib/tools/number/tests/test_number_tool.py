import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.number.number_tool import NumberTool


class TestNumberTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        self.assertEqual(NumberTool.num2ordinal(2), "2nd")
        self.assertEqual(NumberTool.num2ordinal(13), "13th")
        self.assertEqual(NumberTool.num2ordinal(101), "101st")
