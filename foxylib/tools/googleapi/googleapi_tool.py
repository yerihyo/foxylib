import os
from functools import reduce

from google.auth.transport import Request

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)


class GoogleapiTool:
    @classmethod
    def credentials2refreshed(cls, creds):
        creds.refresh(Request())
        return creds

