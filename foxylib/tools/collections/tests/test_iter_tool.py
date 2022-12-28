import logging
import sys
from functools import lru_cache
from pprint import pprint
from unittest import TestCase

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class A:
    init_counter = 0
    enter_counter = 0
    exit_counter = 0

    def __init__(self):
        cls = self.__class__
        cls.init_counter += 1
        self.id = cls.init_counter

        # if self.__class__.init_counter == 1:
        #     raise Exception()
        print("__init__ #{}".format(self.init_counter), file=sys.stderr)

    def __enter__(self):
        self.enter_counter += 1
        print("__enter__", file=sys.stderr)

        return self

    def __exit__(self, type, value, tb):
        self.exit_counter += 1
        print("__exit__", file=sys.stderr)

    @classmethod
    @lru_cache(maxsize=1)
    def f(cls):
        logger = FoxylibLogger.func_level2logger(cls.f, logging.DEBUG)

        logger.debug({"START":"START"})
        # return cls()
        with cls() as a:
            while True:
                yield a

class TestIterTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        # a1 = A.f()
        # a2 = A.f()
        logger.debug({"START":"a1"})
        a1 = next(A.f())

        logger.debug({"START": "a2"})
        a2 = A()

        logger.debug({"START": "a3"})
        a3 = next(A.f())

        logger.debug({"a1":a1, "a2":a2})
        self.assertEqual(a1.id, a3.id)
        self.assertNotEqual(a2.id, a3.id)

        self.assertEqual(a1.enter_counter, 1)
        self.assertEqual(a2.enter_counter, 0)
        self.assertEqual(a3.enter_counter, 1)

        self.assertEqual(a1.exit_counter, 0)
        self.assertEqual(a2.exit_counter, 0)
        self.assertEqual(a3.exit_counter, 0)

        ## WARNING: __exit__ is not called!!!!!!!
        # https://stackoverflow.com/questions/21297026/python-destructor-basing-on-try-finally-yield

    def test_02(self):
        hyp = IterTool.head(5, IterTool.range_inf(),)
        ref = [0, 1, 2, 3, 4]

        self.assertEqual(hyp, ref)

    def test_04(self):
        l = [1, 2, 1, 2, 3, 2, 3, 2]
        hyp = list(IterTool.iter2dict_value2latest_index_series(l))
        ref = [{1: 0},
               {1: 0, 2: 1},
               {1: 2, 2: 1},
               {1: 2, 2: 3},
               {1: 2, 2: 3, 3: 4},
               {1: 2, 2: 5, 3: 4},
               {1: 2, 2: 5, 3: 6},
               {1: 2, 2: 7, 3: 6}]

        # pprint({"hyp":hyp})
        self.assertEqual(hyp, ref)

    def test_05(self):
        hyp = IterTool.value_units2index_largest_fit(4.5, [8,6,2,1])
        ref = 2

        self.assertEqual(hyp, ref)

    def test_06(self):
        self.assertTrue(IterTool.are_all_equal([]))
        self.assertTrue(IterTool.are_all_equal([1, 1, 1, 1, 1]))
        self.assertFalse(IterTool.are_all_equal([1, 1, 1, 1, 2]))

    def test_07(self):
        self.assertTrue(IterTool.is_iterable([1]))
        self.assertTrue(IterTool.is_iterable({1}))
        self.assertTrue(IterTool.is_iterable({1: 1}))
        self.assertTrue(IterTool.is_iterable((1, 2)))
        self.assertTrue(IterTool.is_iterable("hello"))

    def test_08(self):
        self.assertEqual(IterTool.index_first_false([]), 0)
        self.assertEqual(IterTool.index_first_false([False, True]), 0)
        self.assertEqual(IterTool.index_first_false([True, True]), 2)
        self.assertEqual(IterTool.index_first_false([True, False]), 1)
        self.assertEqual(IterTool.index_first_false(i < 3 for i in range(100)), 3)

    def test_09(self):
        self.assertEqual(IterTool.nth([1, 2, 3], 0), 1)
        self.assertEqual(IterTool.nth([1, 2, 3], 1), 2)
        self.assertEqual(IterTool.nth([1, 2, 3], 2), 3)
        self.assertIsNone(IterTool.nth([1, 2, 3], 3))

    def test_10(self):
        f_checkers = [
            lambda x: x < 2,
            lambda x: x < 1,
            lambda x: x < 8,
        ]
        bucket_indexes = list(IterTool.values2bucketindexes(range(10), f_checkers))
        self.assertEqual(bucket_indexes, [0, 0, 2, 2, 2, 2, 2, 2, 3, 3])
