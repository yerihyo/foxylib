import logging
from types import FunctionType, MethodType
from unittest import TestCase

from nose.tools import assert_is_not_none

from foxylib.tools.function.callable_tool import CallableTool
from foxylib.tools.function.method_tool import MethodTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


def my_function():
    def inner_function():
        pass

    return inner_function

my_inner_function = my_function()

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

        self.assertTrue(isinstance(my_inner_function, FunctionType))
        self.assertFalse(isinstance(my_inner_function, MethodType))
        self.assertFalse(hasattr(my_inner_function, "__self__"))

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


class TestCallableTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(CallableTool.callable2type(my_function), CallableTool.Type.FUNCTION)
        self.assertEqual(CallableTool.callable2type(my_inner_function), CallableTool.Type.FUNCTION)
        self.assertEqual(CallableTool.callable2type(MyObject.mystaticmethod), CallableTool.Type.FUNCTION)

        obj1 = MyObject()
        self.assertEqual(CallableTool.callable2type(obj1.myinstancemethod), CallableTool.Type.INSTANCEMETHOD)
        self.assertEqual(CallableTool.callable2type(MyObject.myclassmethod), CallableTool.Type.CLASSMETHOD)
        self.assertEqual(CallableTool.callable2type(obj1.myclassmethod), CallableTool.Type.CLASSMETHOD)


    def test_02(self):
        def fx(func):
            self.assertEqual(CallableTool.callable2type(func), CallableTool.Type.FUNCTION)

        def fy(func):
            self.assertEqual(CallableTool.callable2type(func), CallableTool.Type.FUNCTION)

        class A:
            @fx
            def x(self): pass

            @classmethod
            @fy
            def y(cls): pass







