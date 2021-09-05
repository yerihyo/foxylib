import logging
import time
from datetime import datetime
from functools import lru_cache, partial, wraps
from unittest import TestCase

import pytest
import pytz
from cachetools import TTLCache, cached, LRUCache, cachedmethod
from cachetools.keys import hashkey

from foxylib.tools.cache.cache_decorator import CacheDecorator
from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.cache.cachetools.cachetools_tool import CooldownTool
from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class CacheForTest:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
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

        time.sleep(cls.Subtest01Exception.TTL+1)
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

class TestDecorator(TestCase):
    @classmethod
    def subtest_01_function_decorator(cls):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped
        return wrapper

    @classmethod
    def subtest_01_method_decorator(cls):
        def decorator(method):
            @wraps(method)
            def wrapped(self, *args, **kwargs):
                return method(self, *args, **kwargs)
            return wrapped

        return decorator

    @classmethod
    def subtest_01(cls):
        return 1


class TestCache:

    @classmethod
    @lru_cache(maxsize=1)
    def cache_lru_02(cls):
        return LRUCache(maxsize=12)

    @classmethod
    @lru_cache(maxsize=1)
    def cache_lru_03(cls):
        return LRUCache(maxsize=12)





class TestCooldownTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)


    @classmethod
    @CooldownTool.invoke_or_cooldown_error(TTLCache(ttl=2, maxsize=12))
    def subtest_01(cls, k,):
        return 1

    #############################################################
    # CAUTION!!!!!!! memory leak !!!
    # https://github.com/tkem/cachetools/issues/106
    @pytest.mark.skip(reason="memory leak!!!")
    def test_01(self):
        cls = self.__class__

        self.assertEqual(cls.subtest_01("a"), 1)
        with self.assertRaises(CooldownTool.NotCallableException):
            cls.subtest_01("a")

        self.assertEqual(cls.subtest_01("b"), 1)

        time.sleep(2)
        self.assertEqual(cls.subtest_01("a"), 1)


    @classmethod
    @cached(TestCache.cache_lru_02())
    @CooldownTool.invoke_or_cooldown_error(TTLCache(ttl=2, maxsize=12))
    def subtest_02(cls, k,):
        return 2

    #############################################################
    # CAUTION!!!!!!! memory leak !!!
    # https://github.com/tkem/cachetools/issues/106
    @pytest.mark.skip(reason="memory leak!!!")
    def test_02(self):
        cls = self.__class__


        self.assertEqual(cls.subtest_02("a"), 2)
        self.assertEqual(cls.subtest_02("a"), 2)

        TestCache.cache_lru_02().pop(hashkey(cls, "a"))

        with self.assertRaises(CooldownTool.NotCallableException):
            cls.subtest_02("a")

        self.assertEqual(cls.subtest_02("b"), 2)

        ttl = 2
        time.sleep(ttl)
        self.assertEqual(cls.subtest_02("a"), 2)

    @classmethod
    @cached(TestCache.cache_lru_03(),
            key=FunctionTool.func2args_rshifted(hashkey, 1))
    @CooldownTool.invoke_or_cooldown_error(
        TTLCache(ttl=2, maxsize=12),
        key=FunctionTool.func2args_rshifted(hashkey, 1))
    def subtest_03(cls, k, ):
        return 3

    def test_03(self):
        cls = self.__class__

        self.assertEqual(cls.subtest_03("a"), 3)
        self.assertEqual(cls.subtest_03("a"), 3)

        self.assertIn(hashkey("a"), TestCache.cache_lru_03())
        TestCache.cache_lru_03().pop(hashkey("a"))

        with self.assertRaises(CooldownTool.NotCallableException):
            cls.subtest_03("a")

        self.assertEqual(cls.subtest_03("b"), 3)

        # wait out enough
        ttl = 2
        time.sleep(ttl)
        self.assertEqual(cls.subtest_03("a"), 3)

    @classmethod
    @lru_cache(maxsize=1)
    def cache_lru_04(cls):
        return LRUCache(maxsize=12)

    @classmethod
    @cachedmethod(lambda c: c.cache_lru_04())
    @CooldownTool.invoke_or_cooldown_error(
        TTLCache(ttl=2, maxsize=12),
        key=FunctionTool.func2args_rshifted(hashkey,1))
    def subtest_04(cls, k, ):
        return 4

    #############################################################
    # WARNING! cachedmethod is NOT an IDEAL APPROACH BUT WORKS W/O MEMORY LEAK. RECOMMENDED IF NEED TO POP lru_cache
    # cachedmethod can be tricky since it's a function. func2args_rshifted() preferred.
    def test_04(self):
        cls = self.__class__

        self.assertEqual(cls.subtest_04("a"), 4)
        self.assertEqual(cls.subtest_04("a"), 4)

        cls.cache_lru_04().pop(hashkey("a"))

        with self.assertRaises(CooldownTool.NotCallableException):
            cls.subtest_04("a")

        self.assertEqual(cls.subtest_04("b"), 4)

        ttl = 2
        time.sleep(ttl)
        self.assertEqual(cls.subtest_04("a"), 4)



    @classmethod
    @lru_cache(maxsize=1)
    def cache_lru_05(cls):
        return LRUCache(maxsize=12)

    @classmethod
    @lru_cache(maxsize=1)
    def cache_cooldown_05(cls):
        return TTLCache(ttl=2, maxsize=12)

    @classmethod
    @cachedmethod(lambda c: c.cache_lru_05()) # cachedmethod can be tricky since it's a function. func2args_rshifted() preferred.
    @CooldownTool.invoke_or_cooldown_error_cachedmethod(lambda c: c.cache_cooldown_05())
    def subtest_05(cls, k, ):
        return 5

    #############################################################
    # WARNING! NOT RECOMMENDED APPROACH
    # cachedmethod can be tricky since it's a function. func2args_rshifted() preferred.
    def test_05(self):
        cls = self.__class__

        self.assertEqual(cls.subtest_05("a"), 5)
        self.assertEqual(cls.subtest_05("a"), 5)

        cls.cache_lru_05().pop(hashkey("a"))

        with self.assertRaises(CooldownTool.NotCallableException):
            cls.subtest_05("a")

        self.assertEqual(cls.subtest_05("b"), 5)

        ttl = 2
        time.sleep(ttl)
        self.assertEqual(cls.subtest_05("a"), 5)



    @classmethod
    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1),)
    def subtest_06(cls, x):
        return x

    def test_06(self):
        cls = self.__class__
        cls.subtest_06(5)

        cache1 = CacheManager.callable2cache(cls.subtest_06)
        self.assertEqual(len(cache1), 1)
        self.assertEqual([(5,)], list(cache1.keys()))

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=5),
                                      cachedmethod=partial(CacheDecorator.cachedmethod_each, indexes_each=[1]),
                                      )
    def subtest_08(self, l):
        return l

    def test_08(self):
        logger = FoxylibLogger.func_level2logger(self.test_08, logging.DEBUG)

        self.subtest_08([1,2,3])

        cache = CacheManager.callable2cache(self.subtest_08)

        self.assertTrue(cache)
        logger.debug({"cache":cache})

        self.assertEqual(len(cache), 3)
        self.assertEqual([(1,),(2,),(3,)], list(cache.keys()))
        self.assertEqual(cache[(1,)], 1)
        self.assertEqual(cache[(2,)], 2)
        self.assertEqual(cache[(3,)], 3)

        CacheManager.add2cache(self.subtest_08, 5, args=[4])
        self.assertEqual(self.subtest_08([4]), [5])

    @cached(LRUCache(maxsize=10),
            key=FunctionTool.func2args_rshifted(hashkey, 1))
    def subtest_09(self, x):
        return datetime.now(pytz.utc)

    def test_09(self):
        dt_01 = self.subtest_09(1)
        dt_02 = self.subtest_09(1)
        self.assertEqual(dt_01, dt_02)

        dt_03 = self.subtest_09(2)
        self.assertNotEqual(dt_01, dt_03)

    @classmethod
    @cached(LRUCache(maxsize=10),
            key=FunctionTool.func2args_rshifted(hashkey, 1))
    def subtest_10(cls, x):
        return datetime.now(pytz.utc)

    def test_10(self):
        cls = self.__class__
        dt_01 = cls.subtest_10(1)
        dt_02 = cls.subtest_10(1)
        self.assertEqual(dt_01, dt_02)

        dt_03 = cls.subtest_10(2)
        self.assertNotEqual(dt_01, dt_03)

