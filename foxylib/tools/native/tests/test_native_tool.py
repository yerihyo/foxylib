import logging
from unittest import TestCase

from future.utils import lfilter, lmap

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import BooleanTool


class TestBooleanTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(BooleanTool.parse2nullboolean(True), True)
        self.assertEqual(BooleanTool.parse2nullboolean(False), False)
        self.assertEqual(BooleanTool.parse2nullboolean(None), None)

        self.assertEqual(BooleanTool.parse2nullboolean("YES"), True)
        self.assertEqual(BooleanTool.parse2nullboolean("y"), True)
        self.assertEqual(BooleanTool.parse2nullboolean("t"), True)
        self.assertEqual(BooleanTool.parse2nullboolean("true"), True)

        self.assertEqual(BooleanTool.parse2nullboolean("No"), False)
        self.assertEqual(BooleanTool.parse2nullboolean("n"), False)
        self.assertEqual(BooleanTool.parse2nullboolean("f"), False)
        self.assertEqual(BooleanTool.parse2nullboolean("false"), False)
        self.assertEqual(BooleanTool.parse2nullboolean(""), False)




