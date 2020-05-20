import logging
from unittest import TestCase

from foxylib.tools.function.method_tool import MethodTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class MyObject:
    @classmethod
    def myclassmethod(cls):
        pass

    def myinstancemethod(self):
        pass


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




