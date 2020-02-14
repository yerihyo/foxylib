import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.inspect.inspect_tool import InspectTool


class TestInspectTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        x = None

        hyp = InspectTool.variable2name(x)
        ref = "x"
        self.assertEqual(hyp, ref)
