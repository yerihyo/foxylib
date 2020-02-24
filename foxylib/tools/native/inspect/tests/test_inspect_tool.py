import inspect
import logging
from functools import partial
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.inspect.inspect_tool import InspectTool


def function():
    pass

class A:
    @staticmethod
    def _staticmethod():
        pass

    @classmethod
    def _classmethod(cls):
        pass

    def _objectmethod(self):
        return "a"


class TestInspect(TestCase):
    def test_01(self):
        self.assertIs(inspect.ismethod(A._staticmethod), False)
        self.assertIs(inspect.isfunction(A._staticmethod), True)

        self.assertIs(inspect.ismethod(partial(A._staticmethod)()), False)
        self.assertIs(inspect.isfunction(partial(A._staticmethod)()), False)

        self.assertIs(inspect.ismethod(A._classmethod), True)
        self.assertIs(inspect.isfunction(A._classmethod), False)

        self.assertIs(inspect.ismethod(A._objectmethod), False)
        self.assertIs(inspect.isfunction(A._objectmethod), True)

        a = A()
        self.assertIs(inspect.ismethod(a._objectmethod), True)
        self.assertIs(inspect.isfunction(a._objectmethod), False)


        self.assertIs(inspect.ismethod(function), False)
        self.assertIs(inspect.isfunction(function), True)

        self.assertEqual(A._objectmethod(a), "a")
        self.assertIs(inspect.ismethod(partial(A._objectmethod, a)), False)
        self.assertIs(inspect.isfunction(partial(A._objectmethod, a)), False)

class TestInspectTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        x = None

        hyp = InspectTool.variable2name(x)
        ref = "x"
        self.assertEqual(hyp, ref)
