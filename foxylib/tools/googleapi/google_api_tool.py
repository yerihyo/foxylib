from __future__ import print_function

from google.auth.transport.requests import Request

from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.pickle.pickle_tool import PickleTool


class CredentialCache:

    @classmethod
    def filepath2cachefuncs_pickle(cls, filepath):
        f_load = lambda: PickleTool.file2obj(filepath)
        f_save = lambda cred: PickleTool.obj2file(filepath, cred)
        return f_load, f_save


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

