import logging
import re
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import StringTool


class TestContextfreeTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        p1 = re.compile(r"\s+")
        hyp1 = StringTool.str_span_pair2is_deliminated("hello world", [(0,5), (6,11)], p1)
        self.assertTrue(hyp1,)

        p2 = re.compile(r"")
        hyp2 = StringTool.str_span_pair2is_deliminated("hello world", [(0, 5), (6, 11)], p2)
        self.assertFalse(hyp2, )

        p3 = re.compile(r"\s*")
        hyp3 = StringTool.str_span_pair2is_deliminated("hello world", [(0, 5), (6, 11)], p3)
        self.assertTrue(hyp3, )

    def test_02(self):
        p1 = re.compile(r"\s+")
        spans_pair1 = [[(0,1),(4,5)], [(2,3)]]
        hyp1 = list(StringTool.str_spans_list2j_tuples_delimited("a b c d e", spans_pair1, p1))
        self.assertEqual(hyp1,[(0,0)])

        spans_pair2 = [[(0, 1), (6, 7),(8,9)], [(2, 3),(4,5)]]
        hyp2 = list(StringTool.str_spans_list2j_tuples_delimited("a b c d e", spans_pair2, p1))
        self.assertEqual(hyp2, [(0, 0)])

        spans_pair3 = [[(2, 3), (4, 5)], [(0, 1), (6, 7), (8, 9)], ]
        hyp3 = list(StringTool.str_spans_list2j_tuples_delimited("a b c d e", spans_pair3, p1))
        self.assertEqual(hyp3, [(1, 1)])

        spans_pair4 = [[(2, 3), (4, 5)], [(8, 9), (0, 1), (6, 7), ], ]
        hyp4 = list(StringTool.str_spans_list2j_tuples_delimited("a b c d e", spans_pair4, p1))
        self.assertEqual(hyp4, [(1, 2)])

        spans_pair5 = [[(2, 3), (6, 7)], [(8, 9), (0, 1), (4, 5), ], [(6, 7)]]
        hyp5 = list(StringTool.str_spans_list2j_tuples_delimited("a b c d e", spans_pair5, p1))
        self.assertEqual(hyp5, [(0, 2, 0)])
