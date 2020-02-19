import logging
from unittest import TestCase

from foxylib.tools.arithmetic.arithmetic_tool import ArithmeticTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestArithmeticTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(ArithmeticTool.divide_and_ceil(10, 3), 4)