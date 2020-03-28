import logging
from unittest import TestCase

from wtforms import Form
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.wtforms.wtforms_tool import WTFormsTool


class TestWTFormsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
        WTFormsTool.json_init()

    def test_01(self):
        class TestForm(Form):
            email = EmailField()

        form = TestForm()
        hyp = WTFormsTool.boundfield2name(form.email)
        ref = "email"

        self.assertEqual(hyp, ref)

    def test_02(self):

        field_label_value_list = [
            ("youtube_input", URLField(label="youtube_input", validators=[DataRequired()]), "")]
        form = WTFormsTool.field_label_value_list2form_dummy(field_label_value_list)
        is_valid = form.youtube_input.validate(form, )

        self.assertFalse(is_valid)
        self.assertIn("youtube_input", form.errors)
