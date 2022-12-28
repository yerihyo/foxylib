# from __future__ import annotations
import logging
import unittest
from dataclasses import dataclass, fields, Field, asdict, make_dataclass, \
    _FIELDS
from pprint import pprint
from typing import List, Optional
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
        A = DataclassTool.schema2dataclass_tree('A', schema)
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

    @unittest.skip(reason="can't make it work")
    def test_08(self):

        class A: pass

        @dataclass(frozen=True)
        class A:
            x: int
            a: Optional[A] = None

        a = from_dict(A, {'x':3, 'a':{'x':4,}})
        self.assertTrue(a.x, 3)
        # self.assertTrue(a.a_list[0].x, 4)
        # self.assertTrue(a.a_list[1].x, 5)

    def test_09(self):

        class A:
            @dataclass(frozen=True)
            class B:
                y: str

        @dataclass(frozen=True)
        class A:
            x: int
            bs: List[A.B]

        a = from_dict(A, {'x':3, 'bs':[{'y':'a'}, {'y':'b'}]})
        self.assertTrue(a.x, 3)
        self.assertTrue(a.bs[0].y, 'a')
        self.assertTrue(a.bs[1].y, 'b')

    def test_10(self):

        class A:
            @dataclass(frozen=True)
            class B:
                y: str

        @dataclass(frozen=True)
        class A:
            x: int
            bs: List[A.B]

        a = from_dict(A, {'x': 3, 'bs': [{'y': 'a'}, {'y': 'b'}]})
        a2 = DataclassTool.jpath2replaced(a, ['bs', 0, 'y'], 'c')
        self.assertTrue(a2.bs[0].y, 'c')

        b = from_dict(A, {'x': 3, 'bs': [{'y': 'a'}, {'y': 'b'}]})
        b2 = DataclassTool.jpaths2replaced(b, [(['bs', 0, 'y'], 'p'), (['bs', 1, 'y'], 'q')])
        self.assertTrue(b2.bs[0].y, 'p')
        self.assertTrue(b2.bs[1].y, 'q')
