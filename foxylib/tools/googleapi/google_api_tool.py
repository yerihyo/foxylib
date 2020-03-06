from __future__ import print_function

import pickle
from functools import wraps

from cachetools import TTLCache, Cache
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from nose.tools import assert_is_not_none

from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.pickle.pickle_tool import PickleTool


class GoogleAPITool:
    class Scope:
        DRIVE = "https://www.googleapis.com/auth/drive"
        DRIVE_READONLY = "https://www.googleapis.com/auth/drive.readonly"

        SPREADSHEETS_READONLY = "https://www.googleapis.com/auth/spreadsheets.readonly"

        YOUTUBE_READONLY = "https://www.googleapis.com/auth/youtube.readonly"

    @classmethod
    def file_scope2flowrun_local_server(cls, filepath_credentials_json, scopes):
        def flowrun(*_, **__):
            flow = InstalledAppFlow.from_client_secrets_file(filepath_credentials_json, scopes)
            return flow.run_local_server(*_, **__)
        return flowrun

    @classmethod
    def file_scope2flowrun_console(cls, filepath_credentials_json, scopes):
        def flowrun(*_, **__):
            flow = InstalledAppFlow.from_client_secrets_file(filepath_credentials_json, scopes)
            return flow.run_console(*_, **__)
        return flowrun

    @classmethod
    def j_credentials2client_id(cls, credentials):
        return JsonTool.down(credentials, ["installed","client_id"])

    @classmethod
    def flowrun_cachefile2credentials(cls, flowrun, filepath_cache, ):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        cred = PickleTool.file2obj(filepath_cache)
        if cred and cred.valid:
            return cred

        # If there are no (valid) credentials available, let the user log in.
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            cred = flowrun()

        PickleTool.obj2file(filepath_cache, cred)

        return cred

class Tmp:
    @classmethod
    def credential_flowrun2updated(cls, credential, flowrun):
        _c = credential

        if _c and _c.valid:
            return _c, False

        # If there are no (valid) credentialentials available, let the user log in.
        if _c and _c.expired and _c.refresh_token:
            _c.refresh(Request())
        else:
            _c = flowrun(*_, **__)

        return _c, True

    @classmethod
    def cache_flowrun2mongo(cls, flowrun=None, collection=None,):
        assert_is_not_none(collection)

        def wrapper(f):
            @wraps(f)
            def wrapped(j_credentials, scope, *_, **__):
                client_id = GoogleAPITool.j_credentials2client_id(j_credentials)

                doc = collection.get({"client_id":client_id, "scope":scope})
                cred_in = pickle.loads(doc["bytes"])

                cred_out, updated = GoogleAPITool.credential_flowrun2updated(cred_in, f)

                if updated:
                    collection.put({"client_id":client_id, "scope":scope, "bytes":pickle.dumps(cred_out)})

                return cred_out

            return wrapped

        return wrapper(flowrun) if flowrun else wrapper



