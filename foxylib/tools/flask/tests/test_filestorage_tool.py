import filecmp
import logging
import os
from unittest import TestCase

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.flask.filestorage_tool import FilestorageTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestFilestorageTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        filepath_in = os.path.join(FILE_DIR, 'data', 'test_01.jpeg')
        with FilestorageTool.filepath2filestorage(filepath_in) as storage:
            filepath_out = os.path.join(FILE_DIR, 'data', 'test_01.out.jpeg')
            storage.save(filepath_out)

        self.assertTrue(filecmp.cmp(filepath_in, filepath_out))

    def test_02(self):
        filepath_in = os.path.join(FILE_DIR, 'data', 'test_01.jpeg')
        with FilestorageTool.filepath2filestorage(filepath_in) as storage:
            bytes_hyp = storage.read()

        bytes_ref = FileTool.filepath2bytes(filepath_in)
        self.assertEqual(bytes_hyp, bytes_ref)
