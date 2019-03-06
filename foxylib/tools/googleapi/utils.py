from __future__ import print_function

import os

from nose.tools import assert_true
from oauth2client import file, client, tools

from foxylib.tools.file.file_tools import makedirs_if_empty
from foxylib.tools.log.logger_tools import LoggerToolkit, FoxylibLogger

FILE_PATH = os.path.normpath(os.path.realpath(__file__))
FILE_DIR = os.path.dirname(FILE_PATH)
LIB_DIR = os.path.dirname(FILE_DIR)
SRC_DIR = os.path.dirname(LIB_DIR)
WEB_DIR = os.path.join(SRC_DIR,'web')
DATA_DIR = os.path.join(WEB_DIR,'data')
STATIC_DIR = os.path.join(WEB_DIR,"static")
CONFIG_DIR = os.path.join(WEB_DIR,"config")
TMP_DIR = os.path.join(WEB_DIR,"tmp")

# SERVICE LIST
# https://developers.google.com/api-client-library/python/apis/

class GoogleAPIToolkit:
    class Scope:
        DRIVE = "drive"
        DRIVE_READONLY = "drive.readonly"
        SPREADSHEETS_READONLY = "spreadsheets.readonly"

    @classmethod
    def scope2url(cls, str_scope):
        return "https://www.googleapis.com/auth/{0}".format(str_scope)

    @classmethod
    def filepath_pair_scope2creds(cls, filepath_credentials_json, filepath_token_json, str_scope):
        assert_true(os.path.exists(os.path.dirname(filepath_token_json)))

        storage = file.Storage(filepath_token_json)
        creds = storage.get() if os.path.exists(filepath_token_json) else None

        if not creds or creds.invalid:
            url_scope = cls.scope2url(str_scope)
            flow = client.flow_from_clientsecrets(filepath_credentials_json, url_scope)
            creds = tools.run_flow(flow, storage)
        return creds

scope2url = GoogleAPIToolkit.scope2url


# def username2filepath_credentials_json(username_GOOGLE):
#     return os.path.join(CONFIG_DIR, "google","api", "{0}.credentials.json".format(username_GOOGLE))
    
# def username_scope2filepath_token_json(username_GOOGLE, str_scope):
#     return os.path.join(TMP_DIR, "google","api", username_GOOGLE, "{0}.token.json".format(str_scope))

# def scope_str2url(str_scope): return "https://www.googleapis.com/auth/{0}".format(str_scope)

# @LoggerToolkit.DurationWrapper.info(func2logger=FoxylibLogger.func2logger)
# def username_scope2creds(username_GOOGLE,
#                          str_scope,
#                          ):
#
#     filepath_credentials_json = username2filepath_credentials_json(username_GOOGLE)
#     filepath_token_json = username_scope2filepath_token_json(username_GOOGLE, str_scope)
#     makedirs_if_empty(os.path.dirname(filepath_token_json))
#
#     store = file.Storage(filepath_token_json)
#     creds = store.get() if os.path.exists(filepath_token_json) else None
#
#     if not creds or creds.invalid:
#         url_scope = scope_str2url(str_scope)
#         flow = client.flow_from_clientsecrets(filepath_credentials_json, url_scope)
#         creds = tools.run_flow(flow, store)
#     return creds


