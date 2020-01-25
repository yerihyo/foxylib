import logging
import re
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import format_str


class TestRegexTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp1 = format_str(r"{}{{2,}}", r"a")
        ref1 = r"a{2,}"
        self.assertEqual(hyp1, ref1)

        m = re.match(hyp1, "aaa")
        self.assertTrue(m)
