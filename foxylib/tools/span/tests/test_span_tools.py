import logging
from unittest import TestCase

from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.span.span_tools import SpanToolkit


class TestSpanToolkit(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        span_list = [(0,3), (6,8), (18,19), (24,27), (28,29),(30,31),(32,33), (49,50)]
        hyp = SpanToolkit.span_list_limit2span_best(span_list, 20)
        ref = (30,50)

        self.assertEqual(hyp, ref)
