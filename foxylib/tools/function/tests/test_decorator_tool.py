import logging
import sys
from functools import lru_cache
from unittest import TestCase

from foxylib.tools.function.decorator_tool import DecoratorTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class TestDecoratorTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @classmethod
    @DecoratorTool.override_result(func_override=lambda clazz, x, *_, **__: x)
    def f_01(cls, x, y):
        return y

    def test_01(self):
        self.assertEqual(self.__class__.f_01(1,2), 1)
