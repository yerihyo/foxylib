import logging
import os
from unittest import TestCase

from jinja2 import Template, escape
from markupsafe import Markup

from foxylib.tools.jinja2.jinja2_tool import Jinja2Renderer, Jinja2Tool_Deprecated, Jinja2Tool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class Jinja2Test(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_00(self):
        self.assertEqual('<b><a>a</a></b>!', Markup('<b><a>a</a></b>!'))
        self.assertFalse(Jinja2Tool.equal('<b><a>a</a></b>!', Markup('<b><a>a</a></b>!')))
        self.assertEquals('<b><a>a</a></b>!', '<b><a>a</a></b>!')

    def test_01(self):
        hyp_01 = Template('<b>{{ name }}</b>!').render(name="<a>a</a>")
        self.assertEquals(hyp_01, "<b><a>a</a></b>!")

        hyp_02 = Template('<b>{{ name }}</b>!').render(name=Markup("<a>a</a>"))
        self.assertEquals(hyp_02, "<b><a>a</a></b>!")

        hyp_03 = Template('<b>{{ name }}</b>!').render(name=escape("<a>a</a>"))
        self.assertEquals(hyp_03, '<b>&lt;a&gt;a&lt;/a&gt;</b>!')

        hyp_04 = Template('<b>{{ name }}</b>!').render(name=escape(Markup("<a>a</a>")))
        self.assertEquals(hyp_04, "<b><a>a</a></b>!")


        hyp_11 = Template(Markup('<b>{{ name }}</b>!')).render(name="<a>a</a>")
        self.assertEquals(hyp_11, "<b><a>a</a></b>!")



        hyp_21 = Template(Markup('<b>{{ name }}</b>!'), autoescape=True).render(name="<a>a</a>")
        self.assertEquals(hyp_21, "<b>&lt;a&gt;a&lt;/a&gt;</b>!")


class Jinja2ToolTest(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertTrue(Jinja2Tool.equal("a", "a"))
        self.assertFalse(Jinja2Tool.equal("a", "b"))

        self.assertTrue(Jinja2Tool.equal(Markup("a"), Markup("a")))
        self.assertFalse(Jinja2Tool.equal(Markup("a"), Markup("b")))

        self.assertFalse(Jinja2Tool.equal("a", Markup("a")))
        self.assertFalse(Jinja2Tool.equal("a", Markup("b")))


class Jinja2RendererTests(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = Jinja2Renderer.text2text('<b>{{ name }}</b>!', {"name":"<a>a</a>"})
        self.assertTrue(Jinja2Tool.equal(hyp, "<b><a>a</a></b>!"))

    def test_02(self):
        hyp_01 = Jinja2Renderer.markup2markup(Markup('<b>{{ name }}</b>!'), {"name":"<a>a</a>"})
        self.assertTrue(Jinja2Tool.equal(hyp_01, Markup('<b>&lt;a&gt;a&lt;/a&gt;</b>!')))

        hyp_02 = Jinja2Renderer.markup2markup(Markup('<b>{{ name }}</b>!'), {"name": Markup("<a>a</a>")})
        self.assertTrue(Jinja2Tool.equal(hyp_02, Markup('<b><a>a</a></b>!')))

    def test_03(self):
        filepath = os.path.join(FILE_DIR, "test.txt")
        hyp_01 = Jinja2Renderer.textfile2text(filepath, {"name":"<a>a</a>"})
        self.assertTrue(Jinja2Tool.equal(hyp_01, '<b><a>a</a></b>!'))

    def test_04(self):
        filepath = os.path.join(FILE_DIR, "test.txt")
        hyp_01 = Jinja2Renderer.htmlfile2markup(filepath, {"name":"<a>a</a>"})
        self.assertTrue(Jinja2Tool.equal(hyp_01, Markup('<b>&lt;a&gt;a&lt;/a&gt;</b>!')))

        hyp_02 = Jinja2Renderer.htmlfile2markup(filepath, {"name": Markup("<a>a</a>")})
        self.assertTrue(Jinja2Tool.equal(hyp_02, Markup('<b><a>a</a></b>!')))


class Jinja2Tool_DeprecatedTest(TestCase):
    def test_01(self):
        filepath = os.path.join(FILE_DIR,"test.part.txt")
        s = Jinja2Tool_Deprecated.tmplt_file2str(filepath, {"name":"Peter"})
        self.assertEqual("hello, Peter", s)


    def test_02(self):
        filepath = os.path.join(FILE_DIR,"test.part.html")
        s = Jinja2Tool_Deprecated.tmplt_file2html(filepath, {"name":"Peter"})
        self.assertEqual("<a>hello, Peter</a>", s)


    def test_03(self):
        filepath = os.path.join(FILE_DIR,"test.part.html")
        s = Jinja2Tool_Deprecated.tmplt_file2str(filepath, {"name":"Peter"})
        self.assertEqual("<a>hello, Peter</a>", s)

    def test_04(self):
        filepath = os.path.join(FILE_DIR,"test.part.html")
        s = Jinja2Tool_Deprecated.tmplt_file2html(filepath, {"name":"<b>b</b>"})
        self.assertEqual("<a>hello, Peter</a>", s)

