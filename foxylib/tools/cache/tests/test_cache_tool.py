import logging
import sys
from collections import Counter
from functools import lru_cache
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class C:
    def __init__(self, v):
        self.call_count = {}
        self.v = v

    @lru_cache(maxsize=1)
    def f(self, x):
        self.call_count[x] = self.call_count.get(x, 0) + 1
        print(x, file=sys.stderr)
        return self.v + x


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        c1 = C(1)
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.f(2), 3)
        self.assertEqual(c1.call_count, {1: 1, 2: 1})

        c2 = C(2)
        self.assertEqual(c2.f(3), 5)
        self.assertEqual(c2.f(2), 4)
        self.assertEqual(c2.f(1), 3)
        self.assertEqual(c2.f(2), 4)
        self.assertEqual(c2.f(1), 3)
        self.assertEqual(c2.f(3), 5)
        self.assertEqual(c2.call_count, {1: 1, 2: 1, 3: 2})

    def test_02(self):
        c1 = C(1)
        c2 = C(2)
        c3 = C(3)
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.call_count, {1: 1,})

        self.assertEqual(c2.f(1), 3)
        self.assertEqual(c2.call_count, {1: 1, })

        self.assertEqual(c3.f(1), 4)
        self.assertEqual(c3.call_count, {1: 1, })

        """
        cache fail!!
        """
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.call_count, {1: 2, })  # 1's call_count is 2. cache fail!
