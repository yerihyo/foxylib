import logging
from pprint import pformat
from typing import List, Any, Tuple

from future.utils import lmap, lfilter
from googleapiclient.discovery import build

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key, DictTool, zip_strict
from foxylib.tools.collections.groupby_tool import DuplicateTool
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class GsheetsTool:
    @classmethod
    def sheets(cls, service, spreadsheet_id, ):
        # service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, includeGridData=False)
        response = request.execute()

        return response.get('sheets')

    @classmethod
    def dict_sheetname2sheetprops(cls, service, spreadsheet_id):
        logger = FoxylibLogger.func_level2logger(cls.dict_sheetname2sheetprops, logging.DEBUG)

        hdocs_sheet = cls.sheets(service, spreadsheet_id)
        hdocs_sheetproperty = lmap(lambda x:x['properties'], hdocs_sheet)

        """
        {
            "sheetId": 1,
            "title": "2021.04.03 Tahoe",
            "index": 1,
            "sheetType": "GRID",
            "gridProperties": {
              "rowCount": 20,
              "columnCount": 6,
              "frozenRowCount": 1
            }
          }
          """
        dict_out = IterTool.iter2dict(hdocs_sheetproperty, lambda x:x['title'])
        # logger.debug(pformat({
        #     'hdocs_sheetproperty':hdocs_sheetproperty,
        #     'dict_out':dict_out,
        # }))

        return dict_out

    @classmethod
    def sheetname2sheetid(cls, service, spreadsheet_id, sheet_name):
        logger = FoxylibLogger.func_level2logger(cls.sheetname2sheetid, logging.DEBUG)

        dict_sheetname2sheetprops = cls.dict_sheetname2sheetprops(service, spreadsheet_id)
        sheet_id = JsonTool.down(dict_sheetname2sheetprops, [sheet_name, 'sheetId'])
        return sheet_id

    @classmethod
    def sheet2name(cls, sheet):
        return JsonTool.down(sheet, ['properties', 'title'])

    @classmethod
    def sheetnames(cls, service, spreadsheet_id,):
        sheets = cls.sheets(service, spreadsheet_id)
        return lmap(cls.sheet2name, sheets)

    """
    reference: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear
    """
    @classmethod
    def sheet_clear_or_skip(cls, service, spreadsheet_id, sheetname):
        logger = FoxylibLogger.func_level2logger(cls.sheet_clear_or_skip, logging.DEBUG)
        sheets = cls.sheets(service, spreadsheet_id)

        sheet = IterTool.filter2single_or_none(lambda sheet: cls.sheet2name(sheet) == sheetname, sheets)
        if not sheet:
            return

        h = {"spreadsheetId": spreadsheet_id,
             'range': sheetname,
             }
        result = service.spreadsheets().values().clear(**h).execute()
        return result

    @classmethod
    def sheet_delete_or_skip(cls, service, spreadsheet_id, sheetname):
        # service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        sheets = cls.sheets(service, spreadsheet_id)

        sheet = IterTool.filter2single_or_none(lambda sheet: cls.sheet2name(sheet) == sheetname, sheets)
        if not sheet:
            return

        body = {
            'requests': [{
                'deleteSheet': {
                    'sheetId': JsonTool.down(sheet, ['properties', 'sheetId'])
                }
            }]
        }
        request = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body,
        )
        response = request.execute()

        return response

    @classmethod
    def sheet_create_or_skip(cls, service, spreadsheet_id, sheetname):
        # service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        sheetnames = cls.sheetnames(service, spreadsheet_id)
        if sheetname in sheetnames:
            return

        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheetname
                    }
                }
            }]
        }
        request = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body,
        )
        response = request.execute()

        return response


    @classmethod
    def colindex2name(cls, colindex) -> str:
        q, r = divmod(colindex, 26)
        ch = chr(ord('A') + r)

        if not q:
            return ch
        return cls.colindex2name(q-1) + ch

    @classmethod
    def point2str_A1(cls, point:Tuple[int,int]) -> str:
        rowindex, colindex = point
        return f'{cls.colindex2name(colindex)}{rowindex+1}'

    @classmethod
    def point2str_R1C1(cls, point: Tuple[int, int]) -> str:
        rowindex, colindex = point
        return f'R{rowindex + 1}C{colindex+1}'

    @classmethod
    def data_ll2str_R1C1(cls, data_ll: List[List[Any]]) -> str:
        rowcount = len(data_ll)
        colcount = max(map(len, data_ll))
        return ':'.join(map(cls.point2str_R1C1, [(0, 0), (rowcount - 1, colcount - 1)]))



    @classmethod
    def sheet_range2data_ll(cls, credentials, spreadsheet_id, range_) -> List[List[str]]:
        logger = FoxylibLogger.func_level2logger(cls.sheet_range2data_ll, logging.DEBUG)
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        return cls.service_range2data_ll(service, spreadsheet_id, range_)

    @classmethod
    def service_range2data_ll(cls, service, spreadsheet_id, range_) -> List[List[str]]:
        logger = FoxylibLogger.func_level2logger(cls.service_range2data_ll, logging.DEBUG)
        h = {"spreadsheetId": spreadsheet_id,
             "range": range_,
             }
        result = service.spreadsheets().values().get(**h).execute()
        values = result.get('values', [])

        # logger.debug({"len(values)":len(values)})

        return values

    @classmethod
    def credentials2service(cls, credentials):
        return build('sheets', 'v4', credentials=credentials, cache_discovery=False)

    """
    reference: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
    """
    @classmethod
    def data_ll2update_range(cls, service, spreadsheet_id, range_, data_ll:List[List[Any]]):
        logger = FoxylibLogger.func_level2logger(cls.sheet_range2data_ll, logging.DEBUG)
        # logger.debug({"spreadsheet_id": spreadsheet_id, "range": range})

        # service = build('sheets', 'v4', http=credentials.authorize(Http()))
        # service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
        value_range = {
            'range': range_,
            "majorDimension": "ROWS",
            'values': data_ll
        }

        h = {"spreadsheetId": spreadsheet_id,
             "range": range_,
             "valueInputOption": "RAW",  # https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
             "body": value_range,
             }
        result = service.spreadsheets().values().update(**h).execute()
        # values = result.get('values', [])

        # logger.debug({"result":result})

        return result

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
