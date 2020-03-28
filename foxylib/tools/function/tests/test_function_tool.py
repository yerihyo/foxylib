import logging
from unittest import TestCase

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFunctionTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)


    def test_01(self):
        def f1():
            return 1

        self.assertEqual(FunctionTool.shift_args(f1, 1)("a"), 1)

    def test_02(self):
        self.assertEqual(FunctionTool.xf2y(3, lambda x:x+1), 4)

    def test_03(self):
        f = lambda x,y:x+y
        self.assertEqual(FunctionTool.f_args2f_tuple(f)((2,3)), 5)

