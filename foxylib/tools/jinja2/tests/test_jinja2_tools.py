import os
from unittest import TestCase

from jinja2 import Template
from markupsafe import Markup

from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class Jinja2ToolTest(TestCase):
    def test_01(self):
        filepath = os.path.join(FILE_DIR,"test.part.txt")
        s = Jinja2Tool.tmplt_file2str(filepath, {"name":"Peter"})
        self.assertEqual("hello, Peter", s)


    def test_02(self):
        filepath = os.path.join(FILE_DIR,"test.part.html")
        s = Jinja2Tool.tmplt_file2html(filepath, {"name":"Peter"})
        self.assertEqual("<a>hello, Peter</a>", s)


    def test_03(self):
        filepath = os.path.join(FILE_DIR,"test.part.html")
        s = Jinja2Tool.tmplt_file2str(filepath, {"name":"Peter"})
        self.assertEqual("<a>hello, Peter</a>", s)

    def test_04(self):
        filepath = os.path.join(FILE_DIR,"test.part.html")
        s = Jinja2Tool.tmplt_file2html(filepath, {"name":"<b>b</b>"})
        self.assertEqual("<a>hello, Peter</a>", s)


    def test_05(self):
        hyp = Markup(Template(Markup('<b>{{ name }}</b>!'), autoescape=True).render(name="<a>a</a>"))
        self.assertEqual(hyp, Markup("<b>&lt;a&gt;a&lt;/a&gt;</b>!"))
