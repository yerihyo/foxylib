import logging
import os
from functools import reduce
from unittest import TestCase
from urllib.parse import urlencode, quote

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import UrlpathTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname, ] * 4, FILE_DIR)


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        self.assertEqual(
            urlencode({'a':'b', 'c':'d&e'}),
            'a=b&c=d%26e',
        )

        self.assertEqual(
            quote('a=b&c=d'),
            'a%3Db%26c%3Dd',
        )
