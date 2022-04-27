import logging
import os
import sys
import time
from collections import Counter
from functools import lru_cache
from unittest import TestCase

from foxylib.tools.cache.cache_tool import CacheTool
from foxylib.tools.datetime.datetime_tool import DateTool, DatetimeTool
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.clazz.class_tool import ClassTool
from foxylib.tools.readwriter.file.file_readwriter import FileReadwriterTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class C:
    def __init__(self, v):
        self.call_count = {}
        self.v = v

    @lru_cache(maxsize=2)
    def f(self, x):
        self.call_count[x] = self.call_count.get(x, 0) + 1
        print(x, file=sys.stderr)
        return self.v + x


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        c1 = C(1)
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.f(2), 3)
        self.assertEqual(c1.call_count, {1: 1, 2: 1})

        c2 = C(2)
        self.assertEqual(c2.f(3), 5)
        self.assertEqual(c2.f(2), 4)
        self.assertEqual(c2.f(1), 3)
        self.assertEqual(c2.f(2), 4)
        self.assertEqual(c2.f(1), 3)
        self.assertEqual(c2.f(3), 5)
        self.assertEqual(c2.call_count, {1: 1, 2: 1, 3: 2})

    def test_02(self):
        c1 = C(1)
        c2 = C(2)
        c3 = C(3)
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.call_count, {1: 1,})

        self.assertEqual(c2.f(1), 3)
        self.assertEqual(c2.call_count, {1: 1, })

        self.assertEqual(c3.f(1), 4)
        self.assertEqual(c3.call_count, {1: 1, })

        """
        cache fail!!
        """
        self.assertEqual(c1.f(1), 2)
        self.assertEqual(c1.call_count, {1: 2, })  # 1's call_count is 2. cache fail!


class TestCacheTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        cls = self.__class__

        filepath = os.path.join(FILE_DIR, 'tmp', ClassTool.cls2name(cls), 'test_01','cache')

        readwriter = FileReadwriterTool.filepath2utf8_readwriter(filepath, )

        v1 = CacheTool.func_or_readwriter(
            lambda: DatetimeTool.datetime2isoformat(DatetimeTool.utc_now_milli()),
            readwriter,
        )

        time.sleep(5)

        v2 = CacheTool.func_or_readwriter(
            lambda: DatetimeTool.datetime2isoformat(DatetimeTool.utc_now_milli()),
            readwriter,
        )

        self.assertEqual(v1,v2)
        self.assertEqual(v1, FileTool.filepath2utf8(filepath))
