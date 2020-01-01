import os
from mimetypes import guess_type
from unittest import TestCase

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestFileTool(TestCase):
    def test_01(self):
        filepath = os.path.join(os.path.dirname(FILE_DIR), "file_tool.py")
        hyp = FileTool.filepath2mimetype(filepath)

        self.assertEqual(hyp, MimetypeTool.V.TEXT_XPYTHON)
