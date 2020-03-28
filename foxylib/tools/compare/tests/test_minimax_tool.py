import logging
from unittest import TestCase

from foxylib.tools.compare.minimax_tool import MinimaxTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestMinimaxTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        l = [0, 1, 2, 3, 9, 0]
        hyp = MinimaxTool.indexes_minimax(l)
        ref = ([0, 5], [4, ])

        # pprint(hyp)
        self.assertEqual(hyp, ref)