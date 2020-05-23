import logging
from types import FunctionType, MethodType
from unittest import TestCase

from foxylib.tools.function.method_tool import MethodTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


def my_function():
    pass

class MyObject:
    @staticmethod
    def mystaticmethod():
        pass

    @classmethod
    def myclassmethod(cls):
        pass

    def myinstancemethod(self):
        pass


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertTrue(isinstance(my_function, FunctionType))
        self.assertFalse(isinstance(my_function, MethodType))
        self.assertFalse(hasattr(my_function, "__self__"))

        self.assertTrue(isinstance(MyObject.mystaticmethod, FunctionType))
        self.assertFalse(isinstance(MyObject.mystaticmethod, MethodType))
        self.assertFalse(hasattr(MyObject.mystaticmethod, "__self__"))

        obj1 = MyObject()
        self.assertFalse(isinstance(obj1.myinstancemethod, FunctionType))
        self.assertTrue(isinstance(obj1.myinstancemethod, MethodType))
        self.assertTrue(hasattr(obj1.myinstancemethod, "__self__"))
        self.assertFalse(isinstance(obj1.myinstancemethod.__self__, type))

        self.assertFalse(isinstance(MyObject.myclassmethod, FunctionType))
        self.assertTrue(isinstance(MyObject.myclassmethod, MethodType))
        self.assertTrue(hasattr(MyObject.myclassmethod, "__self__"))
        self.assertTrue(isinstance(MyObject.myclassmethod.__self__, type))
        self.assertTrue(isinstance(obj1.myclassmethod.__self__, type))







