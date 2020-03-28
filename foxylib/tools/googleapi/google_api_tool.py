from __future__ import print_function

import pickle
import sys
from datetime import datetime, timedelta
from functools import wraps, partial

import jwt
from cachetools import TTLCache, Cache
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from nose.tools import assert_is_not_none, assert_true

from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.pickle.pickle_tool import PickleTool


class CredentialCache:

    @classmethod
    def filepath2cachefuncs_pickle(cls, filepath):
        f_load = lambda: PickleTool.file2obj(filepath)
        f_save = lambda cred: PickleTool.obj2file(filepath, cred)
        return f_load, f_save

    # @classmethod
    # def cache_or_func_decorator(cls, cachefuncs, func=None):
    #     assert_true(cachefuncs)
    #
    #     def wrapper(f):
    #         @wraps(f)
    #         def wrapped(*_, **__):
    #             return cls.cache_or_func2cred(cachefuncs, partial(f,*_, **__))
    #
    #         return wrapped
    #
    #     return wrapper(func) if func else wrapper
    #
    #
    #
    # @classmethod
    # def cachefile_decorator(cls, cachefile, func=None,):
    #     cachefuncs = cls.filepath2cachefuncs_pickle(cachefile)
    #     return cls.cache_or_func_decorator(cachefuncs, func=func)


class GoogleAPITool:
    class Scope:
        DRIVE = "https://www.googleapis.com/auth/drive"
        DRIVE_READONLY = "https://www.googleapis.com/auth/drive.readonly"

        SPREADSHEETS_READONLY = "https://www.googleapis.com/auth/spreadsheets.readonly"

        YOUTUBE_READONLY = "https://www.googleapis.com/auth/youtube.readonly"

    @classmethod
    def cache_or_func2cred(cls, cachefuncs, func):
        f_load, f_save = cachefuncs

        cred = f_load()
        if cred and cred.valid:
            return cred

        # If there are no (valid) credentials available, let the user log in.
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            cred = func()

        f_save(cred)

        return cred

    @classmethod
    def j_credentials2client_id(cls, credentials):
        return JsonTool.down(credentials, ["installed", "client_id"])


    # @classmethod
    # def file_scope2flowrun_local_server(cls, filepath_credentials_json, scopes):
    #     def flowrun(*_, **__):
    #         flow = InstalledAppFlow.from_client_secrets_file(filepath_credentials_json, scopes)
    #         return flow.run_local_server(*_, **__)
    #     return flowrun
    #
    # @classmethod
    # def file_scope2flowrun_console(cls, filepath_credentials_json, scopes):
    #     def flowrun(*_, **__):
    #         flow = InstalledAppFlow.from_client_secrets_file(filepath_credentials_json, scopes)
    #         return flow.run_console(*_, **__)
    #     return flowrun



    # @classmethod
    # def wrap_flowrun_with_cache(cls, flowrun, cachefuncs, ):
    #     f_load, f_save = cachefuncs
    #
    #     cred = f_load()
    #     if cred and cred.valid:
    #         return cred
    #
    #     # If there are no (valid) credentials available, let the user log in.
    #     if cred and cred.expired and cred.refresh_token:
    #         cred.refresh(Request())
    #     else:
    #         cred = flowrun()
    #
    #     f_save(cred)
    #
    #     return cred
    #
    # @classmethod
    # def flowrun_cachefile2credentials(cls, flowrun, filepath_cache, ):
    #     # The file token.pickle stores the user's access and refresh tokens, and is
    #     # created automatically when the authorization flow completes for the first
    #     # time.
    #     cachefuncs = CredentialCache.filepath2cachefuncs_pickle(filepath_cache)
    #     return cls.wrap_flowrun_with_cache(flowrun, cachefuncs)



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



