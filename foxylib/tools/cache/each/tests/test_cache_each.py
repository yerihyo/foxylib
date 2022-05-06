import logging
import time
from datetime import datetime
from unittest import TestCase

from cachetools import LRUCache
from future.utils import lmap

from foxylib.tools.cache.each.cache_each import CacheEach
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestCacheEach(TestCase):
    @classmethod
    @CacheEach.cached_each(LRUCache(4), indexes_each=[1])
    def subtest_1(cls, l):
        return lmap(lambda x: datetime.now(), range(len(l)))

    def test_1(self):
        logger = FoxylibLogger.func_level2logger(self.test_1, logging.DEBUG)

        [v1, v2, v3] = self.subtest_1([1, 2, 3])
        time.sleep(0.002)
        [w1, w4, w3] = self.subtest_1([1, 4, 3])
        time.sleep(0.002)
        [x5] = self.subtest_1([5])
        time.sleep(0.002)
        [y1] = self.subtest_1([1])
        [z2] = self.subtest_1([2])

        self.assertEqual(v1, w1)
        self.assertEqual(v3, w3)
        self.assertLess(v2, w4)
        self.assertLess(w4, x5)
        self.assertEqual(v1, y1)
        self.assertLess(v2, z2)

