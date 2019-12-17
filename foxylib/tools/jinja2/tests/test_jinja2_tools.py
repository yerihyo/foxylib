import os
from unittest import TestCase

from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class Jinja2ToolTest(TestCase):
    def test_01(self):
        filepath = os.path.join(FILE_DIR,"test_01.part.txt")
        s = Jinja2Tool.tmplt_file2str(filepath, {"name":"Peter"})
        self.assertEquals("hello, Peter", s)
