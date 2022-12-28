import logging
import os
from functools import reduce
from pprint import pprint
from unittest import TestCase

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytest
from googleapiclient.http import MediaFileUpload

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.data.dataapi_tool import DataapiTool, LiveStreamingData
from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 7, FILE_PATH)


class TestNative(TestCase):
    @pytest.mark.skip(reason="upload slow. too much quota (1600)")
    def test_1_upload(self):
        # https://www.youtube.com/watch?v=CxRIcOLLWZk
        logger = FoxylibLogger.func_level2logger(self.test_1_upload, logging.DEBUG)

        # video_id = 'ePnWBJnj7C0'
        credentials = FoxylibGoogleapi.ServiceAccount.credentials(
            scopes=["https://www.googleapis.com/auth/youtube.upload"],
        )

        # str_SCOPE = "drive.readonly"
        # creds = GSSTool.username_scope2creds(FoxylibGoogleapi.OAuth.username(), str_SCOPE)
        # service = build('drive', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        youtube_service = YoutubeapiTool.credentials2service(credentials)

        request = youtube_service.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": "22",
                    "description": "Description of uploaded video.",
                    "title": "Test video upload.",
                    # 'liveBroadcastContent':'upcoming',
                },
                "status": {
                    "privacyStatus": "private",
                }
            },

            # TODO: For this request to work, you must replace "YOUR_FILE"
            #       with a pointer to the actual file you are uploading.
            media_body=MediaFileUpload("/Users/moonyoungkang/Downloads/lightning.mp4")
        )
        response = request.execute()

        print(response)


class TestDataapiTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='"activeLiveChatId" seems to have TTL. disappeared after not using for long time')
    def test_01(self):
        # https://www.youtube.com/watch?v=nHRKoNOQ56w
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        video_id = 'SXfFccUDK68'
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        youtube_service = YoutubeapiTool.credentials2service(credentials)
        data = DataapiTool.video_id2live_streaming_data(video_id, youtube_service)
        logger.debug({'data':data})
        chat_id = LiveStreamingData.data2chat_id(data)

        # ref = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        ref = 'Cg0KC1NYZkZjY1VESzY4KicKGFVDYVlIYkVkcHJ1VFd5QkwxV0xHSHRidxILU1hmRmNjVURLNjg'
        self.assertEqual(chat_id, ref)

    # ptah-dev
    # livestream data
    @pytest.mark.skip(reason="'video_id' keep changing")
    def test_02(self):
        # https://www.youtube.com/watch?v=CxRIcOLLWZk
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        video_id = 'ePnWBJnj7C0'
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        youtube_service = YoutubeapiTool.credentials2service(credentials)
        data = DataapiTool.video_id2live_streaming_data(video_id, youtube_service)
        chat_id = LiveStreamingData.data2chat_id(data)

        # logger.debug({'chat_id':chat_id})
        # ref = 'Cg0KC0N4UkljT0xMV1prKicKGFVDTDI5X1pkaENHV3pjMTZ1NW04S19VURILQ3hSSWNPTExXWms'
        ref = 'Cg0KC2VQbldCSm5qN0MwKicKGFVDTDI5X1pkaENHV3pjMTZ1NW04S19VURILZVBuV0JKbmo3QzA'
        self.assertEqual(chat_id, ref)

