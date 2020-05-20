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
        @CacheManager.attach2method(self2cache=lambda x: LRUCache(maxsize=2), )
        @CacheManager.cachedmethod2use_manager(cachedmethod=cachedmethod)
        def func(self, x):
            print({"x": x}, file=sys.stderr)
            return x

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cls = self.__class__

        obj1 = cls.TestClass()
        obj1.func(3)

        logger.debug({"obj1":obj1, "obj1.func": obj1.func})

        cache1 = CacheManager.callable2cache(obj1.func)
        self.assertEqual(len(cache1), 1)
        self.assertIn((3,), cache1)

        obj2 = cls.TestClass()
        obj2.func(2)

        manager2 = CacheManager.callable2manager(obj2.func)
        cache2 = CacheManager.manager2cache(manager2)
        self.assertEqual(len(cache2), 1)
        self.assertIn((2,), cache2)
        self.assertNotIn((3,), cache2)

        self.assertEqual(len(cache1), 1)
        self.assertIn((3,), cache1)
        self.assertNotIn((2,), cache1)

        CacheManager.add2cache(manager2, 5, args=[-1])
        self.assertEqual(obj2.func(-1), 5)
