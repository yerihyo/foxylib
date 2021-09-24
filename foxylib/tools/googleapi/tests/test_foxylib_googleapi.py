import logging
import os
from functools import reduce
from unittest import TestCase

import pytest

from foxylib.singleton.test.foxylib_test import FoxylibTest
from foxylib.tools.file.readwriter.pickle_readwriter import PickleReadwriter
from foxylib.tools.google.youtube.youtube_tool import YoutubeTool
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi, FoxytrixyYoutubelive
from foxylib.tools.googleapi.googleapi_tool import GoogleapiTool
from foxylib.tools.googleapi.youtube.livestreaming.livestreamingapi_tool import YoutubeLivechatTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.oauth.oauth2_tool import OAuth2Tool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)

class TestFoxylibGoogleapi(TestCase):
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
        readwriter = PickleReadwriter(FoxytrixyYoutubelive.filepath_token_youtube())
        credentials = OAuth2Tool.creator_refresher_readwriter2credentials(
            create_credentials, refresh_credentials, readwriter)
        print({"credentials": credentials})

    def test_02(self):
        scopes = ["https://www.googleapis.com/auth/youtube"]
        filepath_token = FoxytrixyYoutubelive.filepath_token_youtube()
        credentials = FoxylibGoogleapi.OAuth.scopes_creator_file2credentials(
            scopes, lambda f: f.run_console(), filepath_token)
        print({"credentials": credentials})


class TestFoxytrixyYoutubelive(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        text = "hello world jai;j ajeil;kfn aei;jf lkajs;ifja;efjl"
        response = FoxytrixyYoutubelive.text2livechat(text)

        hyp = YoutubeLivechatTool.item2message(response)
        self.assertEqual(hyp, text,)


