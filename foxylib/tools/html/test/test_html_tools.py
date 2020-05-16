import logging
from unittest import TestCase

from markupsafe import Markup

from foxylib.tools.html.html_tool import wrap_html_tag, escape, join_html
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestHTMLTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = wrap_html_tag("asdaf","a")
        ref = "<a >asdaf</a>"

        self.assertEqual(str(hyp), ref)

    def test_02(self):
        hyp = escape(wrap_html_tag("asdaf","a"))
        ref = "<a >asdaf</a>"

        self.assertEqual(str(hyp), ref)

    # @pytest.mark.skip(reason="currently broken")
    def test_03(self):
        hyp = join_html("<a>", [Markup("<b />"), Markup("<c />")])
        ref = "<b />&lt;a&gt;<c />"

        self.assertEqual(str(hyp), ref)


