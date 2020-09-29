import logging
from dataclasses import dataclass, fields, Field
from unittest import TestCase

from foxylib.tools.collections.collections_tool import smap
from future.utils import lmap

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
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
        self.assertEqual(lmap(lambda x:x.name, fields(a)), ["x","y"])
        self.assertEqual(smap(lambda x: x.name, fields(a)), {"x", "y"})




