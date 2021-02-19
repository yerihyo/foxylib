import logging
from dataclasses import dataclass, fields, Field, asdict, make_dataclass, \
    _FIELDS
from pprint import pprint
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

        @dataclass(frozen=True)
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

        @dataclass(frozen=True)
        class A:
            z: dict
            x: int = None
            y: str = None

        a = from_dict(A, {'x': 1, 'z': {'a': 9}})
        self.assertEqual(a, A(**{'x': 1, 'z': {'a': 9}}))

    def test_03(self):
        schema = [
            ('x', int,),
            ('y', [
                ('i', int,),
                ('j', str,),
            ]),
            ('z', str,),
        ]
        A = DataclassTool.make_dataclass_recursive('A', schema)
        dict_a = {'x': 1, 'y': {'i': 1, 'j': 'hello'}, 'z': 'bye'}
        a = from_dict(A, dict_a)
        self.assertEqual(asdict(a), dict_a)

        dict_y = {'i': 9, 'j': 'oh'}
        Y = DataclassTool.jpath2subdataclass(A, ['y'])
        y = from_dict(Y, dict_y)
        self.assertEqual(asdict(y), dict_y)

        print({'a': a, 'y': y})

    def test_04(self):
        @dataclass(frozen=True)
        class A:
            x: int
            y: make_dataclass("Y", [('i', int,), ('j', str,), ])
            z: str

        dict_a = {'x': 1, 'y': {'i': 1, 'j': 'hello'}, 'z': 'bye'}
        a = from_dict(A, dict_a)
        self.assertEqual(asdict(a), dict_a)

        print({'a': a, })

    def test_05(self):
        logger = FoxylibLogger.func_level2logger(self.test_05, logging.DEBUG)

        @dataclass(frozen=True)
        class A:
            x: int
            y: str

        self.assertEqual(DataclassTool.dataclass2fieldnames(A), {'x', 'y'})
        self.assertEqual(
            DataclassTool.json2filtered(A, {'x': 1, 'y': 'a', 'z': 'adsf'}),
            {'x': 1, 'y': 'a', })

    def test_06(self):
        @dataclass(frozen=True)
        class A:
            x: int

        self.assertEqual(DataclassTool.fieldname2checked(A, 'x'), 'x')

    def test_07(self):
        @dataclass(frozen=True)
        class A:
            x: int

        self.assertTrue(DataclassTool.fieldname2is_valid(A, 'x'))
