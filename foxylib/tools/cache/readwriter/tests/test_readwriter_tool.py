import logging
import os
from datetime import timedelta
from unittest import TestCase

from foxylib.tools.cache.readwriter.readwriter_tool import ReadwriterTool
from foxylib.tools.datetime.datetime_tool import DatetimeTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestReadwriterTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        filepath = os.path.join(FILE_DIR, 'test_01', 'cache')

        readwriter = ReadwriterTool.filepath2readwriter(filepath, timedelta(0))
        ReadwriterTool.readerwriter2wrapped_utf8(readwriter)
        self.assertEqual('a','a')
