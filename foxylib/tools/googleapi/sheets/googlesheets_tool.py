import logging
from pprint import pprint

from future.utils import lmap
from googleapiclient.discovery import build

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key, DictTool, zip_strict
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from httplib2 import Http


class GooglesheetsTool:
    @classmethod
    def sheet_range2data_ll(cls, credentials, spreadsheet_id, range):
        logger = FoxylibLogger.func_level2logger(cls.sheet_range2data_ll, logging.DEBUG)
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

    @classmethod
    def sheet_ranges2data_lll(cls, credentials, spreadsheet_id, ranges=None):
        logger = FoxylibLogger.func_level2logger(cls.sheet_ranges2data_lll, logging.DEBUG)
        logger.debug({"spreadsheet_id": spreadsheet_id, "ranges": ranges})

        # service = build('sheets', 'v4', http=credentials.authorize(Http()))
        service = build('sheets', 'v4', credentials=credentials)

        h = DictTool.filter(lambda k, v: v,
                            {"spreadsheetId": spreadsheet_id,
                             "ranges": ranges,
                             })
        result = service.spreadsheets().values().batchGet(**h).execute()
        # pprint({"result":result})
        values = lmap(lambda h:h.get("values") or [], result.get('valueRanges', []))

        logger.debug({"len(values)": len(values)})

        return values

    @classmethod
    def sheet_ranges2dict_range2data_ll(cls, credentials, spreadsheet_id, ranges):
        data_lll = cls.sheet_ranges2data_lll(credentials, spreadsheet_id, ranges)
        return dict(zip_strict(ranges, data_lll))


    @classmethod
    def data_ll2dict_first_col2rest_cols(cls, data_ll):
        h = merge_dicts([{row[0]: row[1:]} for row in data_ll[1:]],
                        vwrite=vwrite_no_duplicate_key)
        return h
