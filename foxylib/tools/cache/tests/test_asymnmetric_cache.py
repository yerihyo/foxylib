import logging
from functools import lru_cache
from unittest import TestCase

from cachetools import LRUCache

from foxylib.tools.cache.asymmetric_cache import AsymmetricCache
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestAsymmetricCache(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        c = LRUCache(10)

        def reader(cache, x, *_, **__):
            if x == 3:
                raise KeyError(x)

            return cache[(x,)]

        def writer(cache, value, x, *_, **__):
            if x == 2:
                return

            k = (x,)
            cache[k] = value

        @AsymmetricCache.Decorator.cached(cache=c, reader=reader, writer=writer)
        def f(x):
            return x

        c[(1,)] = 2
        self.assertEqual(f(1), 2)
        self.assertEqual(c[(1,)], 2)
        del c[(1,)]
        self.assertEqual(f(1), 1)

        self.assertEqual(f(2), 2)
        self.assertNotIn(2, c)

        self.assertEqual(f(3), 3)
        c[(3,)] = 4
        self.assertEqual(c[(3,)], 4)
        self.assertEqual(f(3), 3)
        self.assertEqual(c[(3,)], 3)

    def test_02(self):

        def reader(cache, x, *_, **__):
            if x == 3:
                raise KeyError(x)

            return cache[(x,)]

        def writer(cache, value, x, *_, **__):
            if x == 2:
                return

            k = (x,)
            cache[k] = value

        class A:
            @lru_cache(maxsize=1)  # memleak possible, but using it only for testing
            def cache(self):
                return LRUCache(10)

            @AsymmetricCache.Decorator.cachedmethod(self2cache=lambda x:x.cache(), reader=reader, writer=writer)
            def f(self, x):
                return x

        a1 = A()
        a2 = A()

        a1.cache()[(1,)] = 2
        self.assertEqual(a1.f(1), 2)
        self.assertEqual(a2.f(1), 1)
        self.assertEqual(a1.cache()[(1,)], 2)
        del a1.cache()[(1,)]
        self.assertEqual(a1.f(1), 1)

        self.assertEqual(a1.f(2), 2)
        self.assertNotIn(2, a1.cache())

        self.assertEqual(a1.f(3), 3)
        a1.cache()[(3,)] = 4
        self.assertEqual(a1.cache()[(3,)], 4)
        self.assertEqual(a1.f(3), 3)
        self.assertEqual(a1.cache()[(3,)], 3)
