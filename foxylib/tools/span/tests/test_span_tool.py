import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.span.span_tool import SpanTool


class TestSpanTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        l = [(0, 2),
             (1, 3),
             (0, 4),
             (2, 5),
             (3, 6),
             ]
        hyp = SpanTool.span_list2indexes_uncovered(l)
        ref = {2, 3, 4}

        self.assertEqual(hyp, ref)

    def test_02(self):
        l = [(0, 4),
             (1, 3),
             (0, 4),
             (2, 5),
             (3, 6),
             ]
        hyp = SpanTool.span_list2indexes_uncovered(l)
        ref = {0, 2, 3, 4}

        self.assertEqual(hyp, ref)

    def test_03(self):
        l = [(0, 4),
             (2, 6),
             (1, 3),
             (0, 4),
             (0, 3),
             ]

        hyp = SpanTool.span_list2indexes_uncovered(l)
        ref = {0, 1, 3}

        self.assertEqual(hyp, ref)

    def test_04(self):
        hyp = list(SpanTool.steps(4.0, 3.0, -1))
        ref = [4.0, 3.0]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_05(self):
        hyp = list(SpanTool.steps(4.0, -1.4, -1))
        ref = [4.0, 3.0, 2.0, 1.0, 0.0, -1.0, -1.4]

        # pprint(hyp)
        self.assertEqual(hyp, ref)
