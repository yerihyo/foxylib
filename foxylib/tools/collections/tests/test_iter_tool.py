import logging
import sys
from functools import lru_cache
from unittest import TestCase

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

