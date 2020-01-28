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

