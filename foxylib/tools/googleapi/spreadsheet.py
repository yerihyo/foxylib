from functools import partial

from future.utils import lmap, lfilter
from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http

from foxylib.tools.collections.collections_tools import list2singleton, lfilter_duplicate, ListToolkit
from foxylib.tools.googleapi.appsscript import AppsscriptToolkit
from foxylib.tools.json.json_tools import JToolkit
from foxylib.tools.log.logger_tools import LoggerToolkit, FoxylibLogger
from foxylib.tools.googleapi.doc import USERNAME_GOOGLE_FOXYTRIXY_BOT
# from foxylib.tools.googleapi.utils import username_scope2creds
from foxylib.tools.native.builtin_tools import izip_strict, lmap_strict, zip_strict
from foxylib.tools.string.string_tools import str2strip



class Spreadsheet:
    #DRIVE = "drive"
    
    SCOPE_READONLY = "spreadsheets.readonly"
    SCOPE_READWRITE = "spreadsheets"
    
    @classmethod
    def QDict_googlespreadsheet_id(cls, gsheet_id):
        return {"spreadsheetId":gsheet_id,}
    QDict_gsheet_id = QDict_googlespreadsheet_id
    
    
#     @classmethod
#     def sheet_id_range2values(cls, service, sheet_id, str_range):
#         h = {"spreadsheetId":sheet_id,
#              "range":str_range,
#              }
#         result = service.spreadsheets().values().get(**h).execute()
#         values = result.get('values', [])
#         return values
    
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
    @LoggerToolkit.SEWrapper.info(func2logger=FoxylibLogger.func2logger)
    def sheet2data_ll(cls, creds, gsheet_id, str_SHEET_RANGE,):
        logger = FoxylibLogger.func2logger(cls.sheet2data_ll)

        logger.info({"gsheet_id":gsheet_id, "str_SHEET_RANGE":str_SHEET_RANGE})
        # username_FXTRX = FoxytrixyBot.USERNAME
        # str_SCOPE = Spreadsheet.SCOPE_READONLY
        # creds = username_scope2creds(username_FXTRX, str_SCOPE)

        f_build = LoggerToolkit.SEWrapper.info(func2logger=FoxylibLogger.func2logger)(build)
        service = f_build('sheets', 'v4', http=creds.authorize(Http()))
        
        h = {"spreadsheetId":gsheet_id,
             "range":str_SHEET_RANGE,
             }
        result = service.spreadsheets().values().get(**h).execute()
        values = result.get('values', [])
        
        logger.info("values(# of lines: {0})".format(len(values)))
        
        return values
    
    class ColHead:
        ATTRNAME_RAW = "raw"
        ATTRNAME_NAME = "name"
        ATTRNAME_JKEY = "jkey"
        ATTRNAME_IS_UNIQUE = "is_unique"
        ATTRNAME_IS_LIST = "is_list"

        class UniqueValidatorException(Exception):
            pass

        @classmethod
        def str_list2check_unique(cls, str_KEY_list, ):
            duplicate_list = lfilter_duplicate(str_KEY_list)
            if duplicate_list:
                raise cls.UniqueValidatorException(duplicate_list)

        @classmethod
        def parse_str2j_colhead(cls, s_IN,):
            s_KEY = str2strip(s_IN)
            if not s_KEY: raise Exception()
            
            is_unique = s_KEY.startswith("*")
            is_list = s_KEY.endswith("[]")
            
            iSTART = 1 if is_unique else 0
            iEND = -2 if is_list else len(s_IN)
            name = s_KEY[iSTART:iEND]
            
            jkey = name.split(".")
            is_unique = s_KEY.startswith("*")
            is_list = s_KEY.endswith("[]")
            
            colhead = {cls.ATTRNAME_RAW:s_IN,
                  cls.ATTRNAME_NAME:name,
                  cls.ATTRNAME_JKEY:jkey,
                  cls.ATTRNAME_IS_UNIQUE:is_unique,
                  cls.ATTRNAME_IS_LIST:is_list,
                  }
            return colhead
        
        @classmethod
        def colhead2s_IN(cls, colhead): return colhead[cls.ATTRNAME_RAW]
        @classmethod
        def colhead2col_name(cls, colhead): return colhead[cls.ATTRNAME_NAME]
        @classmethod
        def colhead2jkey_COL(cls, colhead): return colhead[cls.ATTRNAME_JKEY]
        @classmethod
        def colhead2is_unique_col(cls, colhead): return colhead[cls.ATTRNAME_IS_UNIQUE]
        @classmethod
        def colhead2is_col_list(cls, colhead): return colhead[cls.ATTRNAME_IS_LIST]
        
        
        
        
    @classmethod
    def colhead_str2v(cls, colhead, str_COL):
        if colhead[cls.ColHead.ATTRNAME_IS_LIST]: return str_COL.split(",")
        return str_COL
        
    @classmethod
    def col2j(cls, colhead, v_COL):
        jkey = colhead[cls.ColHead.ATTRNAME_JKEY]
        return JToolkit.jkey_v2json(jkey, v_COL)
        
    @classmethod
    def str_list2j_row(cls, j_colhead_list, str_list_ROW):
        if len(j_colhead_list) != len(str_list_ROW):
            return None # Invalid line
        
        n_COL = list2singleton(lmap(len, [j_colhead_list,str_list_ROW]))
        #logger.info("n_COL({0})".format(n_COL))
        
        iList_VALID = lfilter(lambda i:str_list_ROW[i], range(n_COL))
        
        v_list_VALID = lmap(lambda i: cls.colhead_str2v(j_colhead_list[i], str_list_ROW[i]), iList_VALID)
        #logger.info("v_list_VALID(length:{0})".format(len(v_list_VALID)))
        
        j_list_VALID = [cls.col2j(j_colhead_list[iVALID], v_list_VALID[i])
                        for i, iVALID in enumerate(iList_VALID)]
        #logger.info("j_list_VALID(length:{0})".format(len(j_list_VALID,)))
        
        j_MERGED = JToolkit.merge_list(j_list_VALID)
        return j_MERGED
    


    @classmethod
    def _i2rownum(cls, i): return i+2

    class DataUniqueValidatorException(Exception): pass
    @classmethod
    def data2check_unique(cls, j_colhead_list, str_COL_list_ROW_list):
        # if not cls.ColHead.colhead2is_unique_col(colhead): return

        count_col = len(j_colhead_list)
        j_list_uniq = lfilter(lambda j:cls.ColHead.colhead2is_unique_col(j_colhead_list[j]), range(count_col))
        if not j_list_uniq: return

        count_row = len(str_COL_list_ROW_list)

        tuple_ROW_list = lmap(lambda row:tuple(map(lambda j:row[j], j_list_uniq)), str_COL_list_ROW_list)

        iList_duplicate = sorted(lfilter_duplicate(range(count_row), key=lambda i:tuple_ROW_list[i]),
                                 key=lambda i:(tuple_ROW_list[i],i),
                                 )
        if not iList_duplicate: return
        
        column_name_list = lmap(lambda j: cls.ColHead.colhead2col_name(j_colhead_list[j]), j_list_uniq)
        tuple_ROW_list_duplicate = lmap(partial(ListToolkit.li2v,tuple_ROW_list), iList_duplicate)

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
    @LoggerToolkit.SEWrapper.info(func2logger=FoxylibLogger.func2logger)
    def table_ll2colhead_list_j_list(cls, ll_IN):
        logger = FoxylibLogger.func2logger(cls.table_ll2colhead_list_j_list)
        logger.info({"# rows":len(ll_IN)})
        
        ll_RECT = Spreadsheet._table_ll2rectangle(ll_IN)
        str_list_HEAD, str_COL_list_ROW_list = ll_RECT[0], ll_RECT[1:]
        #str_ll_CLEAN = lfilter(lambda l:l[0], str_ll_RECTANGLE)

        cls.ColHead.str_list2check_unique(str_list_HEAD)
        j_colhead_list = lmap(cls.ColHead.parse_str2j_colhead, str_list_HEAD)
        
        #str_ROW_list_COL_list = lmap(list,zip_strict(*str_COL_list_ROW_list))
        cls.data2check_unique(j_colhead_list, str_COL_list_ROW_list)

        
        j_row_list = lfilter(bool,
                             [cls.str_list2j_row(j_colhead_list, str_COL_list_ROW)
                              for str_COL_list_ROW in str_COL_list_ROW_list])

        return j_colhead_list, j_row_list
    
    # @classmethod
    # def j_row2QDict_cond(cls, model, jkey_UNIQ, j_ROW,):# iCOL_UNIQ):
    #     v_UNIQ = JToolkit.down_or_error(j_ROW, jkey_UNIQ)
    #
    #     QDict_cond = model.jkey_v2QDict(jkey_UNIQ, v_UNIQ)
    #     return QDict_cond
    

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

GSS = Spreadsheet
