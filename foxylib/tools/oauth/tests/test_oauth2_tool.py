import logging
import os
from functools import reduce
from unittest import TestCase

from foxylib.tools.file.readwriter.pickle_readwriter import PickleReadwriter
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.googleapi_tool import GoogleapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.oauth.oauth2_tool import OAuth2Tool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*4, FILE_DIR)


class TestOAuth2Tool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        # -*- coding: utf-8 -*-

        # Sample Python code for youtube.liveStreams.list
        # See instructions for running these code samples locally:
        # https://developers.google.com/explorer-help/guides/code_samples#python

        def create_credentials():
            # Get credentials and create an API client
            scopes = ["https://www.googleapis.com/auth/youtube"]
            flow = FoxylibGoogleapi.OAuth.scopes2credentials_flow(scopes)
            return flow.run_console()

        refresh_credentials = GoogleapiTool.credentials2refreshed
        readwriter = PickleReadwriter(FoxylibGoogleapi.OAuth.filepath_token())
        credentials = OAuth2Tool.gereate_credentials(create_credentials, refresh_credentials, readwriter)
        print({"credentials": credentials})


