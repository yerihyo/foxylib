import logging
import os
from functools import reduce
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import UrlpathTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname, ] * 4, FILE_DIR)

class TestUrlTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = UrlpathTool.filepath_pair2url(FILE_DIR, REPO_DIR, )
        ref = "/foxylib/tools/url/tests/"
        self.assertEqual(hyp, ref)
