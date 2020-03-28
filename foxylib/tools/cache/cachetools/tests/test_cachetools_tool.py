import time
from functools import lru_cache
from unittest import TestCase

import pytest
from cachetools import TTLCache, cached, LRUCache, cachedmethod
from cachetools.keys import hashkey

from foxylib.tools.cache.cachetools.cachetools_tool import CooldownTool, CachetoolsTool
from foxylib.tools.function.function_tool import FunctionTool


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
    @lru_cache(maxsize=2)
    def cache_lru_02(cls):
        return LRUCache(maxsize=12)

    @classmethod
    @lru_cache(maxsize=2)
    def cache_lru_03(cls):
        return LRUCache(maxsize=12)




class TestCooldownTool(TestCase):
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
    @cached(TestCache.cache_lru_03(), key=CachetoolsTool.key4classmethod(hashkey))
    @CooldownTool.invoke_or_cooldown_error(TTLCache(ttl=2, maxsize=12), key=CachetoolsTool.key4classmethod(hashkey))
    def subtest_03(cls, k, ):
        return 3

    def test_03(self):
        cls = self.__class__

        self.assertEqual(cls.subtest_03("a"), 3)
        self.assertEqual(cls.subtest_03("a"), 3)

        TestCache.cache_lru_03().pop(hashkey("a"))

        with self.assertRaises(CooldownTool.NotCallableException):
            cls.subtest_03("a")

        self.assertEqual(cls.subtest_03("b"), 3)

        # wait out enough
        ttl = 2
        time.sleep(ttl)
        self.assertEqual(cls.subtest_03("a"), 3)

    @classmethod
    @lru_cache(maxsize=2)
    def cache_lru_04(cls):
        return LRUCache(maxsize=12)

    @classmethod
    @cachedmethod(lambda c: c.cache_lru_04())
    @CooldownTool.invoke_or_cooldown_error(TTLCache(ttl=2, maxsize=12), key=CachetoolsTool.key4classmethod(hashkey))
    def subtest_04(cls, k, ):
        return 4

    #############################################################
    # WARNING! cachedmethod is NOT an IDEAL APPROACH BUT WORKS W/O MEMORY LEAK. RECOMMENDED IF NEED TO POP lru_cache
    # cachedmethod can be tricky since it's a function. shift_args() preferred.
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
    @lru_cache(maxsize=2)
    def cache_lru_05(cls):
        return LRUCache(maxsize=12)

    @classmethod
    @lru_cache(maxsize=2)
    def cache_cooldown_05(cls):
        return TTLCache(ttl=2, maxsize=12)

    @classmethod
    @cachedmethod(lambda c: c.cache_lru_05()) # cachedmethod can be tricky since it's a function. shift_args() preferred.
    @CooldownTool.invoke_or_cooldown_error_cachedmethod(lambda c: c.cache_cooldown_05())
    def subtest_05(cls, k, ):
        return 5

    #############################################################
    # WARNING! NOT RECOMMENDED APPROACH
    # cachedmethod can be tricky since it's a function. shift_args() preferred.
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




