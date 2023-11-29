import logging
from datetime import datetime
from unittest import TestCase

from babel.dates import format_skeleton

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        self.assertEqual(
            format_skeleton('yMEd', datetime(2007, 4, 1, 12, 30), locale='ko'),
            '2007. 4. 1. (일)',
        )

        self.assertEqual(
            format_skeleton('Bhm', datetime(2007, 4, 1, 12, 30), locale='ko'),
            '',
        )
