import logging
from unittest import TestCase

from werkzeug.utils import secure_filename

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        filename = "V1StGXR8_Z5jdHi6B-myT"
        self.assertEqual(secure_filename(filename), filename)
