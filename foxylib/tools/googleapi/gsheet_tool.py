import re
from functools import partial

from future.utils import lmap, lfilter
from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http

from foxylib.tools.collections.collections_tool import lfilter_duplicate, ListTool, \
    vwrite_no_duplicate_key, merge_dicts, luniq, filter2single_or_none, list2tuple
from foxylib.tools.googleapi.appsscript import AppsscriptToolkit
from foxylib.tools.log.logger_tool import LoggerTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import str2strip


class GSSInfo:
    # (gss_id, sheet_name, range)

    @classmethod
    def args2info(cls, gss_id, sheet_name, range=None,):
        return (gss_id, sheet_name, range)

    @classmethod
    def info2gss_id(cls, gss_info):
        return gss_info[0]

    @classmethod
    def info2sheet_name(cls, gss_info):
        return gss_info[1]

    @classmethod
    def info2sheet_range(cls, gss_info):
        (gss_id, sheet_name, range) = gss_info
        if not range: return sheet_name

        return "#".join([sheet_name, range])


    @classmethod
    def info2gss_id_sheet_name(cls, gss_info):
        return gss_info[0:2]

    @classmethod
    def info2gss_id_sheet_range(cls, gss_info):
        return (gss_info[0], cls.info2sheet_range(gss_info))


class GSSTool:
    #DRIVE = "drive"
    
    SCOPE_READONLY = "spreadsheets.readonly"
    SCOPE_READWRITE = "spreadsheets"

    ATTRNAME_CELLS = "cells"
    
    @classmethod
    def sheet_MERGED2UNMERGED(cls, creds, gsheet_id, sheet_name, str_RANGE=None,):
        sheet_name_TMP = ".".join([sheet_name,"tmp4FoxyTrixy"])
        cls.sheet2unmerged(creds, gsheet_id, sheet_name, gsheet_id, sheet_name_TMP,)
        
        l_RANGE_TMP = [sheet_name_TMP]
        if str_RANGE: l_RANGE_TMP.append(str_RANGE)
        str_SHEET_TMP_RANGE = "!".join(l_RANGE_TMP)
        
        return str_SHEET_TMP_RANGE
        #return cls.range2data_ll(gsheet_id, str_SHEET_TMP_RANGE,)
        
    @classmethod
    @LoggerTool.SEWrapper.info(func2logger=FoxylibLogger.func2logger)
    def creds_sheet2data_ll(cls, creds, gss_info):
        gss_id, sheet_range = GSSInfo.info2gss_id_sheet_range(gss_info)

        logger = FoxylibLogger.func2logger(cls.creds_sheet2data_ll)

        logger.info({"gss_id":gss_id, "sheet_range":sheet_range})
        # username_FXTRX = FoxytrixyBot.USERNAME
        # str_SCOPE = cls.SCOPE_READONLY
        # creds = username_scope2creds(username_FXTRX, str_SCOPE)

        f_build = LoggerTool.SEWrapper.info(func2logger=FoxylibLogger.func2logger)(build)
        service = f_build('sheets', 'v4', http=creds.authorize(Http()))
        
        h = {"spreadsheetId":gss_id,
             "range":sheet_range,
             }
        result = service.spreadsheets().values().get(**h).execute()
        values = result.get('values', [])
        
        logger.info("values(# of lines: {0})".format(len(values)))
        
        return values
    


    @classmethod
    def j_colhead_list_j_row2index_list(cls, j_colhead_list, j_row):
        l = []
        for j_head in j_colhead_list:
            cn = cls.ColHead.j_head2col_name(j_head)

            j_cell = filter2single_or_none(lambda j:cls.Cell.j2cn(j)==cn, j_row)
            if not j_cell: continue

            v = cls.Cell.j2v(j_cell)
            if cls.ColHead.j_head2is_list(j_head):
                l.extend(v)
            else:
                l.append(v)
        return l

    @classmethod
    def str_list2j_row(cls, j_colhead_list, str_list_ROW):
        if len(j_colhead_list) != len(str_list_ROW):
            return None # Invalid line
        
        n_col = len(j_colhead_list)

        k_list_valid = lfilter(lambda k:str_list_ROW[k], range(n_col))
        j_cells = luniq([GSSTool.Cell.parse_str2j(j_colhead_list[k], str_list_ROW[k])
                         for k in k_list_valid],
                        idfun=GSSTool.Cell.j2key)

        # j_row = merge_dicts([{cls.ATTRNAME_CELLS:j_cells},
        #                          ], vwrite=vwrite_no_duplicate_key)
        return j_cells


    @classmethod
    def _i2rownum(cls, i): return i+2

    class DataUniqueValidatorException(Exception): pass
    @classmethod
    def data2check_unique(cls, j_colhead_list, str_COL_list_ROW_list):
        # if not cls.ColHead.j_head2is_key(colhead): return

        count_col = len(j_colhead_list)
        j_list_uniq = lfilter(lambda j:cls.ColHead.j_head2is_key(j_colhead_list[j]), range(count_col))
        if not j_list_uniq: return

        count_row = len(str_COL_list_ROW_list)

        tuple_ROW_list = lmap(lambda row:tuple(map(lambda j:row[j], j_list_uniq)), str_COL_list_ROW_list)

        iList_duplicate = sorted(lfilter_duplicate(range(count_row), key=lambda i:tuple_ROW_list[i]),
                                 key=lambda i:(tuple_ROW_list[i],i),
                                 )
        if not iList_duplicate: return
        
        column_name_list = lmap(lambda j: cls.ColHead.j_head2col_name(j_colhead_list[j]), j_list_uniq)
        tuple_ROW_list_duplicate = lmap(partial(ListTool.li2v,tuple_ROW_list), iList_duplicate)

        h_error = {"column_name_list": column_name_list,
                   "rownum_list_duplicate": lmap(cls._i2rownum, iList_duplicate),
                   "tuple_ROW_list_duplicate": tuple_ROW_list_duplicate,
                   }
        raise cls.DataUniqueValidatorException(h_error)
        
    @classmethod
    def _table_ll2rectangle(cls, str_ll_IN):
        str_ll_CLEAN = lfilter(any, str_ll_IN)
        
        count_COL = len(str_ll_CLEAN[0]) # assume first line is colheads
        
        for str_list in str_ll_CLEAN:
            count_ADD = count_COL - len(str_list)
            str_list.extend([""]*count_ADD)
            
        return str_ll_CLEAN
                
    @classmethod
    @LoggerTool.SEWrapper.info(func2logger=FoxylibLogger.func2logger)
    def table_ll2j_pair(cls, ll_IN):
        logger = FoxylibLogger.func2logger(cls.table_ll2j_pair)
        logger.info({"# rows":len(ll_IN)})
        
        ll_RECT = cls._table_ll2rectangle(ll_IN)
        str_list_HEAD, str_COL_list_ROW_list = ll_RECT[0], ll_RECT[1:]
        cls.ColHead.str_list2check_unique(str_list_HEAD)

        col_count = len(str_list_HEAD)
        j_colhead_list = [cls.ColHead.parse_str2j_colhead(str_list_HEAD[k])
                          for k in range(col_count)]
        
        cls.data2check_unique(j_colhead_list, str_COL_list_ROW_list)

        j_row_list_raw = [cls.str_list2j_row(j_colhead_list, str_COL_list_ROW)
                          for str_COL_list_ROW in str_COL_list_ROW_list]
        j_row_list = lfilter(bool, j_row_list_raw)

        logger.info({"j_row_list[0]": j_row_list[0]})
        return j_colhead_list, j_row_list




    @classmethod
    def data2test(cls, creds, gsheet_id, str_SHEET_RANGE):

        service = build('sheets', 'v4', http=creds.authorize(Http()))
        
        h = {"spreadsheetId":gsheet_id,
             "range":str_SHEET_RANGE,
             }
        result = service.spreadsheets().values().get(**h).execute()
        ll_value = result.get('values', [])
        
        if not ll_value:
            print('No data found.')
        else:
            print('Name, Major:')
            for v_ROW_list in ll_value:
                # Print columns A and E, which correspond to indices 0 and 4.
                print(v_ROW_list)
    
    @classmethod
    def sheet2unmerged(cls, creds, gsheet_id_IN, sheet_name_IN, gsheet_id_OUT, sheet_name_OUT,):
        # from foxylib.tools.googleapi.appsscript import AppsScript
        
        # creds = username_scope2creds("foxytrixy.bot", Spreadsheet.SCOPE_READWRITE)
        service = build('script', 'v1', http=creds.authorize(Http()))

        request = {"function": "run",
                   "parameters": [gsheet_id_IN, sheet_name_IN,
                                  gsheet_id_OUT, sheet_name_OUT,
                                  ],
                   }
        try:
            response = service.scripts().run(body=request,
                                             scriptId=AppsscriptToolkit.SCRIPT_ID_SPREADSHEET2UNMERGE).execute()
            if "error" in response: raise Exception(response)
        except errors.HttpError as error:
            # The API encountered a problem.
            print(error.content)

    class ColHead:
        ATTRNAME_STRING = "string"
        ATTRNAME_NAME = "name"
        ATTRNAME_JKEY = "jkey"
        ATTRNAME_IS_KEY = "is_key"
        ATTRNAME_IS_INDEX = "is_index"
        ATTRNAME_IS_LIST = "is_list"

        # ATTRNAME_LIST_MAXCOUNT = "list_maxcount"

        class UniqueValidatorException(Exception):
            pass

        @classmethod
        def str_list2check_unique(cls, str_KEY_list, ):
            duplicate_list = lfilter_duplicate(str_KEY_list)
            if duplicate_list:
                raise cls.UniqueValidatorException(duplicate_list)

        @classmethod
        def m_prefix2is_unique_index(cls, m):
            if not m:
                return [False, ] * 2

            str_prefix = m.group() if m else ""

            is_unique = "*" in str_prefix
            is_index = "?" in str_prefix

            return (is_unique, is_index)

        @classmethod
        def parse_str2j_colhead(cls, s_IN):
            s_KEY = str2strip(s_IN)
            if not s_KEY: raise Exception()

            m = re.search("^[^0-9a-zA-Z]+", s_IN)
            is_unique, is_index = cls.m_prefix2is_unique_index(m)
            is_list = s_KEY.endswith("[]")

            iSTART = m.end() if m else 0
            iEND = -2 if is_list else len(s_IN)
            name = s_KEY[iSTART:iEND]

            colhead = {cls.ATTRNAME_STRING: s_IN,
                       cls.ATTRNAME_NAME: name,
                       cls.ATTRNAME_IS_KEY: is_unique,
                       cls.ATTRNAME_IS_INDEX: is_index,
                       cls.ATTRNAME_IS_LIST: is_list,
                       }
            return colhead

        @classmethod
        def j_head2col_name(cls, j_head):
            return j_head[cls.ATTRNAME_NAME]

        @classmethod
        def j_head2is_key(cls, j_head):
            return j_head[cls.ATTRNAME_IS_KEY]

        @classmethod
        def j_head2is_list(cls, j_head):
            return j_head[cls.ATTRNAME_IS_LIST]

        @classmethod
        def j_head2is_index(cls, j_head):
            return j_head[cls.ATTRNAME_IS_INDEX]

        @classmethod
        def j_list2name_list_unique(cls, j_head_list):
            return lmap(cls.j_head2col_name, filter(cls.j_head2is_key, j_head_list))

        @classmethod
        def j_list2name_list_index(cls, j_head_list):
            return lmap(cls.j_head2col_name, filter(cls.j_head2is_index, j_head_list))


    class Cell:
        COL_NAME = "col_name"
        VALUE = "value"
        STRING = "string"

        @classmethod
        def parse_str2j(cls, j_colhead, s):
            is_list = GSSTool.ColHead.j_head2is_list(j_colhead)
            v = s.split(",") if is_list else s
            k = GSSTool.ColHead.j_head2col_name(j_colhead)
            return {cls.COL_NAME: k,
                    cls.VALUE: v,
                    cls.STRING: s
                    }

        @classmethod
        def j2cn(cls, j): return j[cls.COL_NAME]

        @classmethod
        def j2v(cls, j): return j[cls.VALUE]

        @classmethod
        def j2s(cls, j): return j[cls.STRING]

        @classmethod
        def j2key(cls, j): return (cls.j2cn(j), list2tuple(cls.j2v(j)))

        @classmethod
        def _j_list2kj_dict(cls, j_row):
            return merge_dicts([{cls.j2cn(j_cell): j_cell} for j_cell in j_row],
                               vwrite=vwrite_no_duplicate_key)

        @classmethod
        def j_list2kv_dict(cls, l):
            h_k2j = cls._j_list2kj_dict(l)
            return merge_dicts([{k: cls.j2v(j)} for k, j in h_k2j.items()],
                               vwrite=vwrite_no_duplicate_key)


GCell = GSSTool.Cell
GHead = GSSTool.ColHead
