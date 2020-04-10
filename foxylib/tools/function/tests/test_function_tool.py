import logging
from pprint import pprint
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

    def subtest_04(self):
        pass

    def test_04(self):
        hyp = FunctionTool.func2module_qualname(self.subtest_04)
        ref = ('foxylib.tools.function.tests.test_function_tool', 'TestFunctionTool.subtest_04')

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    class Test05:
        class A:
            @classmethod
            def subtest_05(cls):
                pass

    def test_05(self):
        hyp = FunctionTool.func2module_qualname(self.Test05.A.subtest_05)
        ref = ('foxylib.tools.function.tests.test_function_tool', 'TestFunctionTool.Test05.A.subtest_05')

        # pprint(hyp)
        self.assertEqual(hyp, ref)

