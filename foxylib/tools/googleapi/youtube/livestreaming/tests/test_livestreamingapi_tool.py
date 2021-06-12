import json
import logging
import os
from unittest import TestCase

import pytest

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi, FoxytrixyYoutubelive
from foxylib.tools.googleapi.youtube.livestreaming.livestreamingapi_tool import LiveChatMessagesTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)




class TestLiveChatMessagesTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='"activeLiveChatId" seems to have TTL. disappeared after not using for long time')
    def test_01(self):
        """
        error message from google
        E       googleapiclient.errors.HttpError: <HttpError 403 when requesting https://youtube.googleapis.com/youtube/v3/liveChat/messages?liveChatId=Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc&part=id%2Csnippet%2CauthorDetails&alt=json returned "The live chat is no longer live.">
        :return:
        """

        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        live_chat_id = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        response = LiveChatMessagesTool.list(credentials, live_chat_id)

        self.assertIn("pollingIntervalMillis", response)
        self.assertIn("nextPageToken", response)
        self.assertIn("items", response)

        logger.debug(json.dumps(response, indent=2))

