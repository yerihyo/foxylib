import logging
from unittest import TestCase

from foxylib.tools.collections.dicttree.dicttree_tool import DicttreeTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDicttreeTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    # def test_01(self):
    #     DicttreeTool.jpath2validated(
    #         {'a':{'b':None}},
    #         ['a','b']
    #     )
    #
    #     with self.assertRaises(Exception):
    #         DicttreeTool.jpath2validated(
    #             {'a': {'b': None}},
    #             ['a', 'c']
    #         )
