from unittest import TestCase

from wtforms import Form
from wtforms.fields.html5 import EmailField

from foxylib.tools.wtforms.wtforms_tool import WTFormsTool


class TestWTFormsTool(TestCase):


    def test_01(self):
        class TestForm(Form):
            email = EmailField()

        form = TestForm()
        hyp = WTFormsTool.boundfield2name(form.email)
        ref = "email"

        self.assertEqual(hyp, ref)

