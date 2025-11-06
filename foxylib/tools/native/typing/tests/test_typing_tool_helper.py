import logging
from typing import Union, List, Any, Callable, Type
from unittest import TestCase

import pytest

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.typing._typing_tool_helper import python_type, \
    is_base_generic, is_qualified_generic, is_generic, is_instance


class TestTypingToolHelper(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(python_type(str), str)
        self.assertEqual(python_type(Union[int,str]), Union)

        with self.assertRaises(NotImplementedError):
            python_type(3)

    @pytest.mark.skip(reason="Skipped due to Python 3.12 migration issues")
    def test_02(self):
        self.assertFalse(is_generic(Any))
        self.assertTrue(is_generic(Union))
        self.assertTrue(is_generic(Callable))
        self.assertTrue(is_generic(Type))

        self.assertTrue(is_generic(List))
        self.assertTrue(is_generic(List[int]))
        self.assertFalse(is_generic(3))

        self.assertTrue(is_base_generic(List))
        self.assertFalse(is_base_generic(3))

        self.assertTrue(is_qualified_generic(List[int]))



    @pytest.mark.skip(reason="Skipped due to Python 3.12 migration issues")
    def test_03(self):
        self.assertTrue(is_instance(3, Any))

