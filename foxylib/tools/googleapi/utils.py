from __future__ import print_function

import os

from nose.tools import assert_true
from oauth2client import file, client, tools


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

