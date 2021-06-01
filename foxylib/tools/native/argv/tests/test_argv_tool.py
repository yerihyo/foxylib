import logging
from unittest import TestCase

from future.utils import lfilter, lmap

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.argv.argv_tool import ArgvTool
from foxylib.tools.native.native_tool import BooleanTool


class TestArgvTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertTrue(
            ArgvTool.argv2is_pytest(['/Users/moonyoungkang/project/foxylib/ptah/venv/bin/pytest', '-x'])
        )



