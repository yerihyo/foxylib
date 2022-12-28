import json
import logging
import os
from unittest import TestCase

import pytest

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi, FoxytrixyYoutubelive
from foxylib.tools.googleapi.youtube.livestreaming.livestreamingapi_tool import YoutubeLivechatTool
from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    # def test_1_list(self):
    #     # https://www.youtube.com/watch?v=CxRIcOLLWZk
    #     logger = FoxylibLogger.func_level2logger(self.test_1_list, logging.DEBUG)
    # 
    #     # video_id = 'ePnWBJnj7C0'
    #     scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    #     credentials = FoxylibGoogleapi.ServiceAccount.credentials(scopes=scopes)
    # 
    #     # str_SCOPE = "drive.readonly"
    #     # creds = GSSTool.username_scope2creds(FoxylibGoogleapi.OAuth.username(), str_SCOPE)
    #     # service = build('drive', 'v3', http=creds.authorize(Http()), cache_discovery=False)
    # 
    #     youtube_service = YoutubeapiTool.credentials2service(credentials)
    #     request = youtube_service.liveBroadcasts().list(
    #         part="snippet,contentDetails,status",
    #         broadcastType="all",
    #         mine=True,
    #     )
    #     response = request.execute()
    # 
    #     print(response)

class TestYoutubeLivechatTool(TestCase):
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
        # live_chat_id = 'Cg0KC3JnWW5DQnBUeVI4KicKGFVDTDI5X1pkaENHV3pjMTZ1NW04S19VURILcmdZbkNCcFR5Ujg'

        response = YoutubeLivechatTool.list(credentials, live_chat_id)

        self.assertIn("pollingIntervalMillis", response)
        self.assertIn("nextPageToken", response)
        self.assertIn("items", response)

        logger.debug(json.dumps(response, indent=2))

