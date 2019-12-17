import pytz

from foxylib.tools.date.pytz_tool import pytz_localize
from foxylib.tools.collections.collections_tool import merge_dicts
from googleapiclient.discovery import build
from httplib2 import Http
from datetime import datetime
import re

class GoogledocTool:
    @classmethod
    def gdoc_id2url(cls, gdoc_id):
        return "https://docs.google.com/document/d/{0}/".format(gdoc_id)

    @classmethod
    def creds_gdoc_id2metadata(cls, creds, gdoc_id, options=None, ):
        str_SCOPE = "drive.readonly"
        service = build('drive', 'v3', http=creds.authorize(Http()))

        h = merge_dicts([{"fileId": gdoc_id, },
                         options,
                         ])
        b = service.files().get(**h).execute()
        return b

    @classmethod
    def creds_gdoc_id2mtime(cls, creds, gdoc_id):
        options = {"fields": "modifiedTime"}

        h = cls.creds_gdoc_id2metadata(creds, gdoc_id, options)
        s_DATETIME = h["modifiedTime"]
        dt_NAIVE = datetime.strptime(s_DATETIME, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt_AWARE = pytz_localize(dt_NAIVE, pytz.utc)
        return dt_AWARE

    @classmethod
    def creds_gdoc_id2utf8(cls, creds, gdoc_id):
        # str_SCOPE = "drive.readonly"
        service = build('drive', 'v3', http=creds.authorize(Http()))

        h = {"fileId": gdoc_id,
             "mimeType": "text/plain",
             }
        b = service.files().export(**h).execute()
        s_GDOC = b.decode('utf-8')

        s_OUT = re.sub("\r\n", "\n", s_GDOC)
        return s_OUT

gdoc_id2url = GoogledocTool.gdoc_id2url
creds_gdoc_id2metadata = GoogledocTool.creds_gdoc_id2metadata
creds_gdoc_id2mtime = GoogledocTool.creds_gdoc_id2mtime
creds_gdoc_id2utf8 = GoogledocTool.creds_gdoc_id2utf8



# https://developers.google.com/apis-explorer/#p/drive/v3/
USERNAME_GOOGLE_FOXYTRIXY_BOT = "foxytrixy.bot"
# def googledocument_id2metadata(gdoc_id, options=None,): # add creds
#     # ?load google port https://asdfasdfa
#
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
# #     username_GOOGLE = "foxytrixy.bot"
#     str_SCOPE = "drive.readonly"
#     creds = username_scope2creds(USERNAME_GOOGLE_FOXYTRIXY_BOT, str_SCOPE)
#     service = build('drive', 'v3', http=creds.authorize(Http()))
#
#     h = merge_dicts([{"fileId":gdoc_id,},
#                      options,
#                      ])
#     b = service.files().get(**h).execute()
#     #s = b.decode('utf-8')
#     return b
#
# def googledocument_id2mtime(gdoc_id):
#     options = {"fields":"modifiedTime"}
#
#     h = googledocument_id2metadata(gdoc_id, options)
#     s_DATETIME = h["modifiedTime"]
#     dt_NAIVE = datetime.strptime(s_DATETIME, "%Y-%m-%dT%H:%M:%S.%fZ")
#     dt_AWARE = pytz_localize(dt_NAIVE, pytz.utc)
#     return dt_AWARE
    

# def googledocument_id2utf8(gdoc_id):
#     # ?load google port https://asdfasdfa
#
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
# #     username_GOOGLE = "foxytrixy.bot"
#     str_SCOPE = "drive.readonly"
#     creds = username_scope2creds(USERNAME_GOOGLE_FOXYTRIXY_BOT, str_SCOPE)
#     service = build('drive', 'v3', http=creds.authorize(Http()))
#
#     h = {"fileId":gdoc_id,
#          "mimeType":"text/plain",
#          }
#     b = service.files().export(**h).execute()
#     s_GDOC = b.decode('utf-8')
#
#     s_OUT = re.sub("\r\n","\n",s_GDOC)
#     return s_OUT


# def googledocument_id2url(gdoc_id):
#     return "https://docs.google.com/document/d/{0}/".format(gdoc_id)

