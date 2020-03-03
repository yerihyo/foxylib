from __future__ import print_function

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

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


