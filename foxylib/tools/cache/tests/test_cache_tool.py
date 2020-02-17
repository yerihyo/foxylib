from time import sleep
from unittest import TestCase

# import ring
from cachetools import cached, TTLCache, LRUCache


class TestNative(TestCase):
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
