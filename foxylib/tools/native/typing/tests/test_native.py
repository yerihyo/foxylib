import logging
from decimal import Decimal
from pprint import pprint
from typing import Union, TypeVar
from unittest import TestCase

from foxylib.tools.native.module.module_tool import ModuleTool

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.typing._typing_tool_helper import python_type
from foxylib.tools.native.typing.typing_tool import TypingTool


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(str.mro(), [str, object])
        self.assertEqual(int.mro(), [int, object])
        self.assertEqual(Decimal.mro(), [Decimal, object])

        with self.assertRaises(AttributeError):
            Union.mro()

        # self.assertEqual(ModuleTool.get_module(TypeVar('T', int, float)), 'typing')

        T = TypeVar('T', int, float)

        TypingTool.is_instance(3, T)
