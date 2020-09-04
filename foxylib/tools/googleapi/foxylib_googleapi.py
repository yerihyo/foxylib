import os
import pickle
from functools import reduce

from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from foxylib.tools.file.file_tool import FileTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)


class FoxylibGoogleapi:
    class OAuth:
        @classmethod
        def filepath_credentials(cls):
            return os.path.join(REPO_DIR, "env", "googleapi", "foxylib.foxylib-test.clientid.credential.json")


        @classmethod
        def scopes2credentials_flow(cls, scopes):
            # Get credentials and create an API client
            # scopes = ["https://www.googleapis.com/auth/youtube"]
            client_secrets_file = cls.filepath_credentials()
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            return flow




    class ServiceAccount:
        @classmethod
        def filepath_privatekey(cls):
            # http://console.cloud.google.com/iam-admin/serviceaccounts/details/112472142364049649520
            return os.path.join(REPO_DIR, "env", "googleapi", "foxylib-ff3a87675bbe.json")

        @classmethod
        def credentials(cls):
            # https://developers.google.com/identity/protocols/oauth2/service-account
            # https://cloud.google.com/docs/authentication/
            return Credentials.from_service_account_file(cls.filepath_privatekey())

