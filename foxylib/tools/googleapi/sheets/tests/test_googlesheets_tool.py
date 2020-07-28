import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.sheets.googlesheets_tool import GooglesheetsTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestGooglesheetsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GooglesheetsTool.sheet_range2data_ll(cred, "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo", "Sheet1")
        ref = [['a', 'b', 'c'], ['d', 'e', 'f']]

        # pprint(hyp)
        self.assertEquals(hyp, ref)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GooglesheetsTool.sheet_ranges2data_lll(cred, "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo", ["Sheet1", "Sheet2","a"])
        ref = [[['a', 'b', 'c'], ['d', 'e', 'f']],
               [['a', 'e'], ['e', 'f'], ['k', 'g']],
               [['z','y']],
               ]

        # pprint(hyp)
        self.assertEquals(hyp, ref)


    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GooglesheetsTool.sheet_ranges2dict_range2data_ll(cred, "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo", ["Sheet1", "Sheet2","a"])
        ref = {"Sheet1":[['a', 'b', 'c'], ['d', 'e', 'f']],
               "Sheet2":[['a', 'e'], ['e', 'f'], ['k', 'g']],
               "a":[['z','y']],
               }

        # pprint(hyp)
        self.assertEquals(hyp, ref)
