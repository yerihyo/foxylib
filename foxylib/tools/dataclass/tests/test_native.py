import logging
from dataclasses import dataclass, fields, field, asdict
from typing import List
from unittest import TestCase

from dacite import from_dict
from future.utils import lmap

from foxylib.tools.collections.collections_tool import smap
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

    def test_02(self):
        @dataclass
        class A:
            x: int = None
            y: str = None

        a = from_dict(A, {'x':1, 'y':'name'})
        self.assertEqual(a.x, 1)
        self.assertEqual(a.y, 'name')

        @dataclass
        class B:
            a: A = None
            b: A = None

        b_dict = {'a': {'x': 1, 'y': 'name'}, 'b': {'x': 2, 'y': 'asdf'}}
        b1 = from_dict(B, b_dict)
        b2 = B(**b_dict)

        self.assertEquals(asdict(b1), b_dict)
        self.assertEquals(asdict(b2), b_dict)

        self.assertEqual(b1.a, A(x=1, y='name'))
        self.assertNotEqual(b2.a, A(x=1, y='name'))

        self.assertEqual(b1.a.x, 1)
        self.assertEqual(b1.a.y, 'name')

        self.assertEqual(b1.b.x, 2)
        self.assertEqual(b1.b.y, 'asdf')

        self.assertEqual(asdict(b1), b_dict)

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_03, logging.DEBUG)

        @dataclass
        class A:
            x: int
            y: List[str] = field(default_factory=list)

        a = A(**{'x': 3})
        self.assertEqual(asdict(a), {'x':3, 'y':[]})
