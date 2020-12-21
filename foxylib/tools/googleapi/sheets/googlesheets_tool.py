import logging
from pprint import pprint

from future.utils import lmap, lfilter
from googleapiclient.discovery import build

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key, DictTool, zip_strict, luniq
from foxylib.tools.collections.groupby_tool import dict_groupby_tree, DuplicateTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from httplib2 import Http


class GooglesheetsTool:
    @classmethod
    def sheet_range2data_ll(cls, credentials, spreadsheet_id, range):
        logger = FoxylibLogger.func_level2logger(cls.sheet_range2data_ll, logging.DEBUG)
        logger.debug({"spreadsheet_id": spreadsheet_id, "range": range})

        # service = build('sheets', 'v4', http=credentials.authorize(Http()))
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

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
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

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


class Cellinfo:
    class Field:
        SHEETNAME = "sheetname"
        ROWINDEX = "rowindex"
        COLINDEX = "colindex"
        CONTENT = "content"

    @classmethod
    def info2sheetname(cls, info):
        return info[cls.Field.SHEETNAME]

    @classmethod
    def info2rowindex(cls, info):
        return info[cls.Field.ROWINDEX]

    @classmethod
    def info2colindex(cls, info):
        return info[cls.Field.COLINDEX]

    @classmethod
    def info2content(cls, info):
        return info[cls.Field.CONTENT]

    @classmethod
    def table_dict2info_iter(cls, dict_sheetname2table):
        for sheetname, table in dict_sheetname2table.items():
            for i, row in enumerate(table):
                for j, cell in enumerate(row):
                    info = {Cellinfo.Field.SHEETNAME: sheetname,
                            Cellinfo.Field.ROWINDEX: i,
                            Cellinfo.Field.COLINDEX: j,
                            Cellinfo.Field.CONTENT: cell
                            }
                    yield info


class GooglesheetsErrorcheck:
    class Default:
        @classmethod
        def cellinfo2is_data(cls, info):
            if Cellinfo.info2rowindex(info) == 0:
                return False

            if Cellinfo.info2colindex(info) == 0:
                return False

            return True


    @classmethod
    def table_list2dict_duplicates(cls, dict_sheetname2table, cellinfo2is_data=None, key=None):
        info_list = lfilter(cellinfo2is_data, Cellinfo.table_dict2info_iter(dict_sheetname2table))

        h_duplicates = DuplicateTool.iter2dict_duplicates(info_list, key=lambda x: key(Cellinfo.info2content(x)))
        return h_duplicates
