import json
import logging
import os
from unittest import TestCase

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi, FoxytrixyYoutubelive
from foxylib.tools.googleapi.youtube.livestreaming.livestreamingapi_tool import LiveChatMessagesTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)




class TestLiveChatMessagesTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        live_chat_id = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        response = LiveChatMessagesTool.list(credentials, live_chat_id)

        self.assertIn("pollingIntervalMillis", response)
        self.assertIn("nextPageToken", response)
        self.assertIn("items", response)

        logger.debug(json.dumps(response, indent=2))

