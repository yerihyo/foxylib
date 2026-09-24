import logging
import math
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.number.number_tool import NumberTool
from foxylib.tools.phonenumber.phonenumber_tool import PhonenumberTool


class TestPhonenumberTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        self.assertEqual(
            PhonenumberTool.number_iso31662e164('010-2736-3820', 'KR'),
            '+821027363820'
        )

        self.assertNotEqual(
            PhonenumberTool.number_iso31662e164('010-2736-3820', 'US'),
            '+821027363820'
        )

        self.assertNotEqual(
            PhonenumberTool.number_iso31662e164('010-2736-3820', 'KR'),
            '+821027363821'
        )

        self.assertEqual(
            PhonenumberTool.number_iso31662e164('+1 412-956-0438', 'US'),
            '+14129560438'
        )

        self.assertEqual(
            PhonenumberTool.number_iso31662e164('+1 412-956-0438', 'KR'),
            '+14129560438'
        )

        self.assertEqual(
            PhonenumberTool.number_iso31662e164('10-2736-3820', 'KR'),
            '+821027363820'
        )

        self.assertEqual(
            PhonenumberTool.number_iso31662e164('+1-412-956-0438', 'KR'),
            '+14129560438'
        )
