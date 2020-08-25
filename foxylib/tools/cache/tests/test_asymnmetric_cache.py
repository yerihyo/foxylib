import logging
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
