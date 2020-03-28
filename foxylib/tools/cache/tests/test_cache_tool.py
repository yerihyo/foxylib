import logging
import sys
from functools import lru_cache
from time import sleep
from unittest import TestCase

# import ring
from cachetools import cached, TTLCache, LRUCache
from cachetools.keys import hashkey

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class CacheForTest:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def cache_default(cls):
        logger = FoxylibLogger.func_level2logger(cls.cache_default, logging.DEBUG)

        # print({"hello":"hello"}, file=sys.stderr)
        # raise Exception()

        return LRUCache(maxsize=256)

class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    #### ring
    # https://stackoverflow.com/questions/51504586/can-one-replace-or-remove-a-specific-key-from-functools-lru-cache
    # https://ring-cache.readthedocs.io/en/stable/ring/func_sync.html

    #### cachetools
    # https://pypi.org/project/cachetools/
    # https://cachetools.readthedocs.io/en/stable/

    class Subtest01Exception(Exception):
        subtest_01_called = False
        TTL = 2

    @classmethod
    # @ring.lru(maxsize=200)
    @cached(cache=TTLCache(maxsize=200, ttl=Subtest01Exception.TTL))
    def subtest_01(cls, x):
        if cls.Subtest01Exception.subtest_01_called:
            raise cls.Subtest01Exception()

        cls.Subtest01Exception.subtest_01_called = True
        return x

    def test_01(self):
        cls = self.__class__
        cls.subtest_01(1)
        cls.subtest_01(1)

        sleep(cls.Subtest01Exception.TTL+1)
        with self.assertRaises(cls.Subtest01Exception):
            cls.subtest_01(1)


    def test_02(self):
        cls = self.__class__

        cache = LRUCache(maxsize=200,)

        @cached(cache=cache)
        def f(x, y=None):
            return 2


        cache[hashkey("a",)] = 3
        cache[hashkey("b",)] = 4
        cache[hashkey("d", y="y")] = 5

        self.assertEqual(f("a"), 3)
        self.assertEqual(f("b"), 4)
        self.assertEqual(f("d", y="y"), 5)
        self.assertEqual(f("c"), 2)
        del cache[hashkey("a",)]

        self.assertEqual(f("a"), 2)
        self.assertEqual(f("b"), 4)

        self.assertEqual(DictTool.pop(cache, hashkey("b",)), 4)
        self.assertEqual(f("b"), 2)



    @classmethod
    @cached(CacheForTest.cache_default())
    def subtest_03(cls, k):
        return "a"

    def test_03(self):
        cls = self.__class__
        CacheForTest.cache_default()[hashkey(cls, "z")] = "z"

        self.assertEqual(cls.subtest_03("z"), "z")
        self.assertEqual(cls.subtest_03("a"), "a")