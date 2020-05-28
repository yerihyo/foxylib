import logging
import sys
from functools import lru_cache
from unittest import TestCase

from cachetools import LRUCache, cachedmethod

from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestCacheManager(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    class TestClass:
        @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=2),)
        def func1(self, x):
            print({"x": x}, file=sys.stderr)
            return x

        @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=2), )
        def func2(self, ):
            print("func2 called", file=sys.stderr)
            return "a"

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cls = self.__class__

        obj1 = cls.TestClass()
        obj1.func1(3)

        logger.debug({"obj1":obj1, "obj1.func1": obj1.func1})

        cache1 = CacheManager.callable2cache(obj1.func1)
        self.assertEqual(len(cache1), 1)
        self.assertIn((3,), cache1)

        obj2 = cls.TestClass()
        obj2.func1(2)

        cache2 = CacheManager.callable2cache(obj2.func1)
        self.assertEqual(len(cache2), 1)
        self.assertIn((2,), cache2)
        self.assertNotIn((3,), cache2)

        self.assertEqual(len(cache1), 1)
        self.assertIn((3,), cache1)
        self.assertNotIn((2,), cache1)

        CacheManager.add2cache(obj2.func1, 5, args=[-1])
        self.assertEqual(obj2.func1(-1), 5)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        cls = self.__class__

        obj1 = cls.TestClass()
        obj1.func2()

        logger.debug({"obj1":obj1, "obj1.func2": obj1.func2})

        cache1 = CacheManager.callable2cache(obj1.func2)
        self.assertEqual(len(cache1), 1)
        self.assertIn(tuple([]), cache1)

        obj2 = cls.TestClass()
        obj2.func2()

        cache2 = CacheManager.callable2cache(obj2.func2)
        self.assertEqual(len(cache2), 1)
        self.assertIn(tuple([]), cache2)

        self.assertEqual(len(cache1), 1)
        self.assertIn(tuple([]), cache1)

        CacheManager.add2cache(obj2.func2, 5, args=[])
        self.assertEqual(obj2.func2(), 5)
