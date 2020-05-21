import logging
from unittest import TestCase

from foxylib.tools.function.method_tool import MethodTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


def decorator_add_a(func):
    func.a = "a"
    return func


class MyObject:
    @classmethod
    @decorator_add_a
    def myclassmethod(cls):
        pass

    @decorator_add_a
    def myinstancemethod(self):
        pass


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        self.assertEqual(MyObject.myclassmethod.a, "a")
        self.assertEqual(getattr(getattr(MyObject, "myclassmethod"), "a"), "a")


class TestMethodTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(MethodTool.method2owner(MyObject.myclassmethod), MyObject)

        obj = MyObject()
        self.assertEqual(MethodTool.method2owner(obj.myinstancemethod), obj)

        with self.assertRaises(AttributeError):
            MethodTool.method2owner(MyObject.myinstancemethod)

    def test_02(self):
        self.assertTrue(MethodTool.method2is_classmethod(MyObject.myclassmethod))
        self.assertFalse(MethodTool.method2is_classmethod(MyObject().myinstancemethod))

        self.assertEqual(getattr(MyObject.myclassmethod, "a"), "a")
        self.assertEqual(getattr(MyObject().myinstancemethod, "a"), "a")






