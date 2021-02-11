import logging
from dataclasses import dataclass, fields, Field
from unittest import TestCase

from dacite import from_dict

from foxylib.tools.collections.collections_tool import smap
from future.utils import lmap

from foxylib.tools.dataclass.dataclass_tool import DataclassTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDataclassTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        @dataclass
        class A:
            x: int = None
            y: str = None

        a = A()
        a.x = 1

        self.assertEqual(a.x, 1)
        DataclassTool.allfields2none(a)
        self.assertIsNone(a.x,)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        @dataclass
        class A:
            x: int = None
            y: str = None

        a = from_dict(A, {'x': 1})
        self.assertEqual(a, A(**{'x':1}))




