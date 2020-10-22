import logging
import re
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import StringTool


class TestStringTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        s_in = 'İstanbul'
        s_out = StringTool.str2charwise_lower_samelength(s_in)

        self.assertEqual(s_out, "İstanbul")
        self.assertEqual(s_in.lower(), "i̇stanbul")

        self.assertNotEqual(len(s_in.lower()), len(s_out))
