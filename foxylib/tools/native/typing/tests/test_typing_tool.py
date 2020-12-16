import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union, Any, List, Dict, DefaultDict, FrozenSet, \
    Set, TypeVar
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.typing._typing_tool_helper import python_type
from foxylib.tools.native.typing.typing_tool import TypingTool


class TestTypingTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertTrue(TypingTool.is_annotation(datetime))
        self.assertTrue(TypingTool.is_annotation(str))
        self.assertTrue(TypingTool.is_annotation(tuple))
        self.assertTrue(TypingTool.is_annotation(Optional[str]))

        class X: pass
        self.assertTrue(TypingTool.is_annotation(X))

        T = TypeVar('T', int, str)
        self.assertTrue(TypingTool.is_annotation(T))

        self.assertFalse(TypingTool.is_annotation(3))
        self.assertFalse(TypingTool.is_annotation('asdf'))
        self.assertFalse(TypingTool.is_annotation(list('asdf')))

    def test_02(self):
        with self.assertRaises(TypingTool.NotAnnotationError):
            TypingTool.get_origin(3)

        with self.assertRaises(TypingTool.NotAnnotationError):
            TypingTool.get_origin(3)

        self.assertIsNone(TypingTool.get_origin(str))
        self.assertIsNone(TypingTool.get_origin(list))
        self.assertIsNone(TypingTool.get_origin(Optional))

        self.assertIs(TypingTool.get_origin(Optional[dict]), Union)
        self.assertIsNone(TypingTool.get_origin(Any), )
        self.assertIsNone(TypingTool.get_origin(Union), )

    def test_03(self):
        self.assertTrue(TypingTool.is_optional(Optional))
        self.assertTrue(TypingTool.is_optional(Optional[str]))
        self.assertTrue(TypingTool.is_optional(Union[None, str]))
        self.assertTrue(TypingTool.is_optional(Union[int, None]))
        self.assertTrue(TypingTool.is_optional(Union[int, str, None]))

        self.assertFalse(TypingTool.is_optional(str))
        self.assertFalse(TypingTool.is_optional(Union[str, int]))

        with self.assertRaises(TypingTool.NotAnnotationError):
            TypingTool.is_optional(3)

    def test_04(self):
        self.assertTrue(TypingTool.is_instance(3, Optional[int]))
        self.assertTrue(TypingTool.is_instance(3, Union[int, str]))
        self.assertTrue(TypingTool.is_instance('3', Union[int, str]))
        self.assertTrue(TypingTool.is_instance(None, Union[int, None]))

        self.assertTrue(TypingTool.is_instance(None, Any))
        self.assertTrue(TypingTool.is_instance(3, Any))

        with self.assertRaises(TypingTool.NotAnnotationError):
            TypingTool.is_instance(3, 3)

    def test_05(self):
        self.assertTrue(TypingTool.is_subtype(DefaultDict, Dict))
        self.assertTrue(TypingTool.is_subtype(
            DefaultDict[int,str], Dict[int,str]))

        self.assertFalse(TypingTool.is_subtype(
            DefaultDict[int, str], Dict[int, Decimal]))

