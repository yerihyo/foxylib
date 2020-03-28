import logging

from googleapiclient.discovery import build

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from httplib2 import Http


class GooglesheetsTool:
    @classmethod
    def cred_id_name2data_ll(cls, credentials, spreadsheet_id, range):
        logger = FoxylibLogger.func_level2logger(cls.cred_id_name2data_ll, logging.DEBUG)
        logger.debug({"spreadsheet_id": spreadsheet_id, "range": range})

        # service = build('sheets', 'v4', http=credentials.authorize(Http()))
        service = build('sheets', 'v4', credentials=credentials)

        h = {"spreadsheetId": spreadsheet_id,
             "range": range,
             }
        result = service.spreadsheets().values().get(**h).execute()
        values = result.get('values', [])

        logger.debug({"len(values)":len(values)})

        return values

