import logging
from pprint import pprint
from unittest import TestCase

from googleapiclient.discovery import build

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.sheets.googlesheets_tool import GooglesheetsTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        service = build('sheets', 'v4', credentials=cred, cache_discovery=False)
        spreadsheet_id = '19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo'

        request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, includeGridData=False)
        response = request.execute()

        pprint(response)

    def test_2(self):
        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        service = build('sheets', 'v4', credentials=cred, cache_discovery=False)

        body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': 'test'
                        }
                    }
                }
            ]
        }
        request = service.spreadsheets().batchUpdate(
            spreadsheetId='19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo',
            body=body,
        )
        response = request.execute()

        pprint(response)


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
        self.assertEqual(hyp, ref)

    def test_4(self):
        self.assertEqual(GooglesheetsTool.colindex2name(0), 'A')
        self.assertEqual(GooglesheetsTool.colindex2name(26), 'AA')
        self.assertEqual(GooglesheetsTool.colindex2name(26 * 26), 'ZA')
        self.assertEqual(GooglesheetsTool.colindex2name(26 + 26 * 26), 'AAA')
        self.assertEqual(GooglesheetsTool.colindex2name(26 + 26 * 26 + 26 * 26 * 26), 'AAAA')

    def test_5(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GooglesheetsTool.data_ll2update_range(
            cred,
            "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo",
            "b",
            [['a', 'b', 'c'], ['d', 'e', 'f']],
        )
        # ref = [['a', 'b', 'c'], ['d', 'e', 'f']]

        # pprint(hyp)
        self.assertEqual(
            hyp,
            {
                'spreadsheetId': '19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo',
                'updatedRange': 'b!A1:C2',
                'updatedRows': 2,
                'updatedColumns': 3,
                'updatedCells': 6,
            }
        )
