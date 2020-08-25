import json
import logging
from unittest import TestCase

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.youtubeapi_tool import DataapiTool, LiveStreamingData, LivestreamingapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDataapiTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        # https://www.youtube.com/watch?v=nHRKoNOQ56w
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        video_id = 'nHRKoNOQ56w'
        data = DataapiTool.video_id2live_streaming_data(video_id)
        chat_id = LiveStreamingData.data2chat_id(data)

        ref = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        self.assertEqual(chat_id, ref)


class TestLivestreamingapiTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        live_chat_id = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        response = LivestreamingapiTool.live_chat_id2response(credentials, live_chat_id)

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
