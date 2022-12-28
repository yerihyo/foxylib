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
        f_traversile = TraversileTool.func2traversile(f, [list])
        self.assertEqual(f_traversile(data_in), [[2,3,4,],[5,6,7]])

        self.assertEqual(TraversileTool.tree2traversed(data_in, f, [list]),
                         [[2, 3, 4, ], [5, 6, 7]],
                         )

        with self.assertRaises(Exception):
            TraversileTool.tree2traversed(data_in, f, [dict])

    def test_02(self):
        f = lambda x: x + 1

        data_in = {'a': 1, 'b': {'c': 2}}
        f_traversile = TraversileTool.func2traversile(f, [dict])
        self.assertEqual(f_traversile(data_in), {'a': 2, 'b': {'c': 3}})

        self.assertEqual(TraversileTool.tree2traversed(data_in, f, [dict]),
                         {'a': 2, 'b': {'c': 3}}
                         )

        with self.assertRaises(Exception):
            TraversileTool.tree2traversed(data_in, f, [list])

    def test_03(self):
        f = lambda x: x+1
        f_traversile = TraversileTool.func2traversile(f)
        data_in = {'a': 1, 'b': {'c': [2, 3]}}
        self.assertEqual(f_traversile(data_in), {'a': 2, 'b': {'c': [3, 4]}})

        self.assertEqual(TraversileTool.tree2traversed(data_in, f,),
                         {'a': 2, 'b': {'c': [3, 4]}},
                         )
