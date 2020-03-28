import logging
import re
from functools import partial
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.nlp.contextfree.contextfree_tool import ContextfreeTool
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.string_tool import StringTool


class TestContextfreeTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    # @pytest.mark.skip(reason="not supported any more")
    # def test_01(self):
    #     span_list = [(0,3), (6,8), (18,19), (24,27), (28,29),(30,31),(32,33), (49,50)]
    #     hyp = SpanTool.span_list_limit2span_best(span_list, 20)
    #     ref = (30,50)
    #
    #     self.assertEqual(hyp, ref)

    def test_01(self):
        f_gap2valid = partial(StringTool.str_span2match_blank, "a b c d e")


        spans_pair1 = [[(0, 1), (4, 5)], [(2, 3)]]
        hyp1 = list(ContextfreeTool.spans_list2reducible_indextuple_list(spans_pair1, f_gap2valid))
        self.assertEqual(hyp1, [(0, 0)])

        spans_pair2 = [[(0, 1), (6, 7), (8, 9)], [(2, 3), (4, 5)]]
        hyp2 = list(ContextfreeTool.spans_list2reducible_indextuple_list(spans_pair2, f_gap2valid))
        self.assertEqual(hyp2, [(0, 0)])

        spans_pair3 = [[(2, 3), (4, 5)], [(0, 1), (6, 7), (8, 9)], ]
        hyp3 = list(ContextfreeTool.spans_list2reducible_indextuple_list(spans_pair3, f_gap2valid))
        self.assertEqual(hyp3, [(1, 1)])

        spans_pair4 = [[(2, 3), (4, 5)], [(8, 9), (0, 1), (6, 7), ], ]
        hyp4 = list(ContextfreeTool.spans_list2reducible_indextuple_list(spans_pair4, f_gap2valid))
        self.assertEqual(hyp4, [(1, 2)])

        spans_pair5 = [[(2, 3), (6, 7)], [(8, 9), (0, 1), (4, 5),], [(6, 7)]]
        hyp5 = list(ContextfreeTool.spans_list2reducible_indextuple_list(spans_pair5, f_gap2valid))
        self.assertEqual(hyp5, [(0, 2, 0)])
