import logging
from unittest import TestCase

from foxylib.tools.collections.traversile.traversile_tool import TraversileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDictTraverseTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        f = lambda x:x+1

        data_in = [[1,2,3],[4,5,6]]
        f_traversile = TraversileTool.func2list_traversile(f)
        self.assertEqual(f_traversile(data_in), [[2,3,4,],[5,6,7]])

    def test_02(self):
        f = lambda x:x+1

        data_in = {'a':1, 'b':{'c':2}}
        f_traversile = TraversileTool.func2dict_traversile(f)
        self.assertEqual(f_traversile(data_in), {'a':2, 'b':{'c':3}})

    def test_03(self):
        f = lambda x:x+1

        f_traversile = TraversileTool.func2traversiled(
            lambda x:x+1, ['list','dict'])
        data_in = {'a':1, 'b':{'c':[2,3]}}
        self.assertEqual(f_traversile(data_in), {'a':2, 'b':{'c':[3,4]}})
