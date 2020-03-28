import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.googleapi.foxylib_google_api import FoxylibGoogleapi
from foxylib.tools.googleapi.sheets.googlesheets_tool import GooglesheetsTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestGooglesheetsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GooglesheetsTool.cred_id_name2data_ll(cred, "1VSDDZiNhGVxrd6camls17A_wxWYX9FEuFP7X4LDLBBI", "Sheet1")
        ref = [['a', 'b', 'c'], ['d', 'e', 'f']]

        # pprint(hyp)
        self.assertEquals(hyp, ref)
