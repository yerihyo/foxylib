from unittest import TestCase

from markupsafe import Markup

from foxylib.tools.html.html_tools import wrap_html_tag, escape, join_html


class HTMLToolkitTest(TestCase):
    def test_01(self):
        hyp = wrap_html_tag("asdaf","a")
        ref = "<a >asdaf</a>"

        self.assertEqual(str(hyp), ref)

    def test_02(self):
        hyp = escape(wrap_html_tag("asdaf","a"))
        ref = "<a >asdaf</a>"

        self.assertEqual(str(hyp), ref)

    def test_03(self):
        hyp = join_html("<a>", [Markup("<b />"), Markup("<c />")])
        ref = "<b />&lt;a&gt;<c />"

        self.assertEqual(str(hyp), ref)


