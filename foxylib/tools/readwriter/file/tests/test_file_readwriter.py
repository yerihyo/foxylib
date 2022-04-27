import logging
import os
from datetime import timedelta
from unittest import TestCase

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.readwriter.file.file_readwriter import FileReadwriterTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestFileReadwriterTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        filepath = os.path.join(FILE_DIR, 'tmp','test_01', 'cache')

        readwriter = FileReadwriterTool.filepath2utf8_readwriter(filepath,)
        readwriter.write('a')
        self.assertEqual(readwriter.read(), 'a')
        self.assertEqual(FileTool.filepath2utf8(filepath), 'a')

    def test_02(self):
        filepath = os.path.join(FILE_DIR, 'tmp','test_02', 'cache')

        iostream = FileReadwriterTool.filepath2iostream(filepath,)
        iostream.write('a'.encode('utf-8'))
        self.assertEqual(iostream.read(), 'a'.encode('utf-8'))
        self.assertEqual(iostream.read().decode('utf-8'), 'a')
        self.assertEqual(FileTool.filepath2utf8(filepath), 'a')
