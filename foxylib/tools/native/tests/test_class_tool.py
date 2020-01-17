import collections
import logging
import os
import sys
from functools import reduce
from typing import DefaultDict
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.class_tool import ClassTool, ModuleTool
from foxylib.tools.native.object_tool import ObjectTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*4, FILE_DIR)

class A:
    _h: DefaultDict = collections.defaultdict(list)

    def __init__(self):
        self.z = "z"

    @classmethod
    def put(cls, k, v):
        cls._h[k] = v

    def lookup(self, k):
        return self._h.get(k)


class TestClassTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        a1 = A()
        A.put("0","0")
        a2 = A()
        a2._h = {}

        logger.debug({"A._h": A._h,
                      "a1._h": a1._h,
                      "a2._h": a2._h,
                      })

        a1.put("1","one")
        logger.debug({"A._h": A._h,
                      "a1._h": a1._h,
                      "a2._h": a2._h,
                      })

        a2.put("2", "TWO")
        logger.debug({"A._h": A._h,
                      "a1._h": a1._h,
                      "a2._h": a2._h,
                      })

        a1.put("0", "zero")
        logger.debug({"A._h": A._h,
                      "a1._h": a1._h,
                      "a2._h": a2._h,
                      })

        a2.put("1", "ONE")
        logger.debug({"A._h": A._h,
                      "a1._h": a1._h,
                      "a2._h": a2._h,
                      })

        logger.debug({"A.__dict__":A.__dict__})
        logger.debug({"a1.__dict__": a1.__dict__})

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        a1 = A()
        a2 = A()
        self.assertTrue(ClassTool.cls_name2has_variable(A, "_h"))
        self.assertFalse(ObjectTool.obj_name2has_variable(a1, "_h"))

        A.put("0", "0")

        self.assertIn("0", A._h)
        self.assertIn("0", a1._h)

        a1._h = {}
        self.assertNotIn("0", a1._h)

        a1.put("1","one")
        self.assertIn("1", A._h)
        self.assertNotIn("1", a1._h)

        a1._h["2"] = "two"
        # self.assertNotIn("2", A._h) # system-dependent ?
        self.assertIn("2", a1._h)

        self.assertIsNotNone(a1.lookup("2"))
        # self.assertIsNone(a2.lookup("2")) # system-dependent ?

class TestModuleTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        hyp = ModuleTool.x2module(self.__class__)
        ref = "foxylib.tools.native.tests.test_class_tool"

        self.assertEqual(hyp, ref)


    def test_02(self):
        cls = self.__class__
        hyp = ModuleTool.class2filepath(cls)
        ref = "/foxylib/tools/native/tests/test_class_tool.py"

        self.assertTrue(hyp.endswith(ref))


    def test_03(self):
        hyp = ModuleTool.func2filepath(self.test_03)
        ref = "/foxylib/tools/native/tests/test_class_tool.py"

        self.assertTrue(hyp.endswith(ref))


    def test_04(self):
        hyp = ModuleTool.x2filepath(self)
        ref = "/foxylib/tools/native/tests/test_class_tool.py"

        self.assertTrue(hyp.endswith(ref))
