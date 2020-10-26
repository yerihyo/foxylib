import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.char.char_tool import CharTool


class TestCharTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(CharTool.add_num2chr('a', 3), 'd')
        self.assertEqual(CharTool.add_num2chr('z', -3), 'w')
