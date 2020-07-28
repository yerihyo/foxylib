import os
from functools import reduce

from google.oauth2.service_account import Credentials

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)


class FoxylibGoogleapi:
    class Oauth:
        @classmethod
        def filepath_credentials(cls):
            return os.path.join(REPO_DIR,"env","googleapi","foxytrixy.bot.credential.json")

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
