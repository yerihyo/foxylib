import logging
from pprint import pprint
from unittest import TestCase

from googleapiclient.discovery import build

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.sheets.gsheets_tool import GsheetsTool
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


    def test_3(self):
        logger = FoxylibLogger.func_level2logger(self.test_3, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        service = build('sheets', 'v4', credentials=cred, cache_discovery=False)

        sheetId = GsheetsTool.sheetname2sheetid(service, '19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo', 'testlink')

        request = service.spreadsheets().batchUpdate(**{
            "spreadsheetId": '19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo',
            "body": {
                "requests": [{
                    'updateCells': {
                        'range': {
                            'sheetId': sheetId,
                            # 'startRowIndex': 0,
                            # 'startColumnIndex': 0,
                        },
                        'fields':'*',
                        'rows': [{
                            'values': [{
                                'userEnteredValue': {'stringValue': """asdf qwer
asdf"""},
                                'textFormatRuns': [
                                    {'startIndex': 0, 'format': {'link': {'uri': 'https://www.google.com'}}},
                                    {'startIndex': 4, },
                                    {'startIndex': 11, 'format': {'link': {'uri': 'https://www.naver.com'}}},
                                ]
                            }]
                        }]
                    }
                }]
            }
        })

        # request = service.spreadsheets().values().update(**{
        #     "spreadsheetId": '19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo',
        #     "range": 'testlink',
        #     "valueInputOption": "USER_ENTERED",
        #     # https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
        #     "body": {
        #         'range': 'testlink',
        #         # "majorDimension": "COLUMNS",
        #         'values': [
        #             [
        #                 {
        #                     'userEnteredValue': {'stringValue': 'asdf qwer asdf'},
        #                     'textFormatRuns': [
        #                         {'startIndex': 0, 'format': {'link': {'uri': 'http:www.google.com'}}},
        #                         {'startIndex': 4, },
        #                     ]
        #                 }
        #             ],
        #         ]
        #     },
        # })
        response = request.execute()

        pprint(response)


class TestGooglesheetsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        logger = FoxylibLogger.func_level2logger(self.test_1, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GsheetsTool.sheet_range2data_ll(cred, "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo", "Sheet1")
        ref = [['a', 'b', 'c'], ['d', 'e', 'f']]

        # pprint(hyp)
        self.assertEquals(hyp, ref)

    def test_2(self):
        logger = FoxylibLogger.func_level2logger(self.test_2, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GsheetsTool.sheet_ranges2data_lll(cred, "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo", ["Sheet1", "Sheet2","a"])
        ref = [[['a', 'b', 'c'], ['d', 'e', 'f']],
               [['a', 'e'], ['e', 'f'], ['k', 'g']],
               [['z','y']],
               ]

        # pprint(hyp)
        self.assertEquals(hyp, ref)


    def test_3(self):
        logger = FoxylibLogger.func_level2logger(self.test_3, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        hyp = GsheetsTool.sheet_ranges2dict_range2data_ll(cred, "19-7_V7N89Tou9v_SeMv4g1AvNZ7rnEdYNCvI9bYFDgo", ["Sheet1", "Sheet2","a"])
        ref = {"Sheet1":[['a', 'b', 'c'], ['d', 'e', 'f']],
               "Sheet2":[['a', 'e'], ['e', 'f'], ['k', 'g']],
               "a":[['z','y']],
               }

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_4(self):
        self.assertEqual(GsheetsTool.colindex2name(0), 'A')
        self.assertEqual(GsheetsTool.colindex2name(26), 'AA')
        self.assertEqual(GsheetsTool.colindex2name(26 * 26), 'ZA')
        self.assertEqual(GsheetsTool.colindex2name(26 + 26 * 26), 'AAA')
        self.assertEqual(GsheetsTool.colindex2name(26 + 26 * 26 + 26 * 26 * 26), 'AAAA')

    def test_5(self):
        logger = FoxylibLogger.func_level2logger(self.test_5, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        service = GsheetsTool.credentials2service(cred)

        hyp = GsheetsTool.data_ll2update_range(
            service,
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
