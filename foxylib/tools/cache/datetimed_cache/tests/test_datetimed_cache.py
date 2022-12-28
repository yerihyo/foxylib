from datetime import datetime, timedelta
import logging
from functools import lru_cache
from unittest import TestCase

import pytz
from cachetools import LRUCache

from foxylib.tools.cache.datetimed_cache.datetimed_cache import DatetimedCache
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDatetimedCache(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        c = LRUCache(10)

        @DatetimedCache.Decorator.cached(cache=c, f_pivot=lambda p, *_, **__: p, key=lambda p, x, *_, **__: x)
        def f(dt_pivot, x):
            return dt_pivot

        dt_01 = datetime.now(pytz.utc)
        self.assertEqual(f(dt_01, 1), dt_01)

        dt_02 = datetime.now(pytz.utc) - timedelta(days=1)
        self.assertEqual(f(dt_02, 1), dt_01)
        self.assertEqual(f(dt_02, 2), dt_02)

        dt_03 = datetime.now(pytz.utc)
        self.assertEqual(f(dt_03, 1), dt_03)

    def test_02(self):
        class A:
            @lru_cache(maxsize=1)  # memleak possible, but using it only for testing
            def cache(self):
                return LRUCache(10)

            @DatetimedCache.Decorator.cachedmethod(self2cache=lambda x: x.cache(),
                                                   f_pivot=lambda p, *_, **__: p,
                                                   key=lambda p, x, *_, **__: x)
            def f(self, dt_pivot, x):
                return dt_pivot

        a1 = A()
        a2 = A()

        dt_01 = datetime.now(pytz.utc)
        self.assertEqual(a1.f(dt_01, 1), dt_01)

        dt_02 = datetime.now(pytz.utc) - timedelta(days=1)
        self.assertEqual(a1.f(dt_02, 1), dt_01)
        self.assertEqual(a2.f(dt_02, 1), dt_02)
        self.assertEqual(a1.f(dt_02, 2), dt_02)

        dt_03 = datetime.now(pytz.utc)
        self.assertEqual(a1.f(dt_03, 1), dt_03)
