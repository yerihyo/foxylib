from googleapiclient.discovery import build
from httplib2 import Http

from foxylib.tools.googleapi.gdoc_tools import USERNAME_GOOGLE_FOXYTRIXY_BOT


class SpreadsheetTest:
    def test_04(self):
        # ?load google port https://asdfasdfa 
        
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
    #     username_GOOGLE = "foxytrixy.bot"
        str_SCOPE = "drive.readonly"
        creds = username_scope2creds(USERNAME_GOOGLE_FOXYTRIXY_BOT, str_SCOPE)
        service = build('drive', 'v3', http=creds.authorize(Http()))
        
        h = {"spreadsheetId":'15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40',
             "range":"field",
             }
        result = service.spreadsheets().values().get(**h).execute()

    def test_02(self):
        if True:
            Spreadsheet.data2test("foxytrixy.bot",
                          Spreadsheet.SCOPE_READONLY,
                          '1klHQnqtdWWdVavz2ElM_twC9LIez8N-2Wt4Fwob5mOY',
                          'consumeable',
                          #'field!A1:D',
                          )

        if True:
            gsheet_id_FIELD = '15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40'
            cls.data2test("foxytrixy.bot",
                          Spreadsheet.SCOPE_READWRITE,
                          gsheet_id_FIELD,
                          'field!A1:D',
                          )

            str_SHEET_TMP_RANGE = cls.sheet_MERGED2UNMERGED(gsheet_id_FIELD, "field")
            creds = FoxyosGoogleAPI.username_scope2creds(FoxyosGoogleAPI.Username.FOXYTRIXY_BOT,
                                                         Spreadsheet.SCOPE_READONLY, )
            ll_value = cls.sheet2data_ll(creds, gsheet_id_FIELD, str_SHEET_TMP_RANGE,)
            print(ll_value)

        if True:
            from unchartedwatersonline.models import Consumeable
            Consumeable.gss2db()
        

