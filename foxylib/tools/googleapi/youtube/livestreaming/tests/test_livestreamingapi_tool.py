import json
import logging
from unittest import TestCase

import pytest

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.livestreaming.livestreamingapi_tool import LiveChatMessagesTool, LiveStreamsTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from foxylib.tools.oauth.oauth2_tool import OAuth2Tool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)




    @pytest.mark.skip(reason="not ready yet")
    def test_02(self):
        # -*- coding: utf-8 -*-

        # Sample Python code for youtube.liveStreams.list
        # See instructions for running these code samples locally:
        # https://developers.google.com/explorer-help/guides/code_samples#python

        scopes = ["https://www.googleapis.com/auth/youtube"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = os.path.join(FILE_DIR, "client_secret_1079655127634-4ju5vdivcevginihl24ufalj2p45etk5.apps.googleusercontent.com.json")

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)

        OAuth2Tool.gereate_credentials()

        """
        https://developers.google.com/people/quickstart/python
        how to store/load cred
        """
        credentials = flow.run_console()

        print({"credentials":credentials})

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.liveStreams().list(
            part="snippet,cdn,contentDetails,status",
            mine=True
        )
        response = request.execute()

        print(response)
        j = {'kind': 'youtube#liveStreamListResponse', 'etag': '0WHaTsEupoxVYeTMmiI2uf3sk0I',
             'pageInfo': {'totalResults': 1, 'resultsPerPage': 5}, 'items': [
                {'kind': 'youtube#liveStream', 'etag': '4kbTuNk-oMhOEN3yXrSH76ecN_k',
                 'id': 'IZ-JmGTFFDg-5Xlf2SfiVA1599141900862615',
                 'snippet': {'publishedAt': '2020-09-03T14:05:01Z', 'channelId': 'UCIZ-JmGTFFDg-5Xlf2SfiVA',
                             'title': 'Default stream key', 'description': 'Description for default stream key',
                             'isDefaultStream': False}, 'cdn': {'format': 'variable', 'ingestionType': 'rtmp',
                                                                'ingestionInfo': {
                                                                    'streamName': 'xpcp-3guk-1ckx-xe2j-a5bw',
                                                                    'ingestionAddress': 'rtmp://a.rtmp.youtube.com/live2',
                                                                    'backupIngestionAddress': 'rtmp://b.rtmp.youtube.com/live2?backup=1',
                                                                    'rtmpsIngestionAddress': 'rtmps://a.rtmps.youtube.com:443/live2',
                                                                    'rtmpsBackupIngestionAddress': 'rtmps://b.rtmps.youtube.com:443/live2?backup=1'},
                                                                'resolution': 'variable', 'frameRate': 'variable'},
                 'status': {'streamStatus': 'ready', 'healthStatus': {'status': 'noData'}}, 'contentDetails': {
                    'closedCaptionsIngestionUrl': 'http://upload.youtube.com/closedcaption?cid=xpcp-3guk-1ckx-xe2j-a5bw',
                    'isReusable': True}}]}



class TestLiveStreamsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        credentials = FoxylibGoogleapi.ServiceAccount.credentials()

        body = {
            "cdn": {
                "frameRate": "60fps",
                "ingestionType": "rtmp",
                "resolution": "1080p"
            },
            "contentDetails": {
                "isReusable": True
            },
            "snippet": {
                "title": "Your new video stream's name",
                "description": "A description of your video stream. This field is optional."
            }
        }
        response = LiveStreamsTool.body2response(credentials, body)
        print(response)

class TestLiveChatMessagesTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        live_chat_id = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        response = LiveChatMessagesTool.live_chat_id2response(credentials, live_chat_id)

        self.assertIn("pollingIntervalMillis", response)
        self.assertIn("nextPageToken", response)
        self.assertIn("items", response)

        logger.debug(json.dumps(response, indent=2))

        # sample = {
        #     "items": [
        #         {
        #             "kind": "youtube#liveChatMessage",
        #             "etag": "JzuhwZbhJliKroOU08bsTfd5ZJU",
        #             "id": "LCC.CjgKDQoLbkhSS29OT1E1NncqJwoYVUNtcmxxRklLX1FRQ3NyM0ZSSGEzT0t3EgtuSFJLb05PUTU2dxJFChpDTVc5aUxPV3Blc0NGYUpEN1FvZDhyOEdzdxInQ0xPb2tPT1ZwZXNDRlFGMG1Bb2RiSEVHRncxNTk3NzY4MjA1Mzcz",
        #             "snippet": {
        #                 "type": "textMessageEvent",
        #                 "liveChatId": "Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc",
        #                 "authorChannelId": "UC2Jrcr57x4TkE57aoR910Og",
        #                 "publishedAt": "2020-08-18T16:30:06.524000Z",
        #                 "hasDisplayContent": true,
        #                 "displayMessage": "!PewDiePie",
        #                 "textMessageDetails": {
        #                     "messageText": "!PewDiePie"
        #                 }
        #             },
        #             "authorDetails": {
        #                 "channelId": "UC2Jrcr57x4TkE57aoR910Og",
        #                 "channelUrl": "http://www.youtube.com/channel/UC2Jrcr57x4TkE57aoR910Og",
        #                 "displayName": "Je\u00e2n Carl\u00f5s Creator",
        #                 "profileImageUrl": "https://yt3.ggpht.com/-6qp4Kut5SPc/AAAAAAAAAAI/AAAAAAAAAAA/piwvIVeiBoY/s88-c-k-no-mo-rj-c0xffffff/photo.jpg",
        #                 "isVerified": false,
        #                 "isChatOwner": false,
        #                 "isChatSponsor": false,
        #                 "isChatModerator": false
        #             }
        #         },
        #     ]
        # }
