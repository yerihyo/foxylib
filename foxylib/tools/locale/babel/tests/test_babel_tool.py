import logging
from datetime import datetime
from unittest import TestCase
import pytest

from babel.dates import format_skeleton

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="Skipped due to Python 3.12 migration issues")
    def test_1(self):
        self.assertEqual(
            format_skeleton('yMEd', datetime(2007, 4, 1, 12, 30), locale='ko'),
            '2007. 4. 1. (일)',
        )

        self.assertEqual(
            format_skeleton('Bhm', datetime(2007, 4, 1, 12, 30), locale='ko'),
            '',
        )
