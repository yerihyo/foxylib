import json
import logging
from unittest import TestCase

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

        chat_id = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        response = LivestreamingapiTool.chat_id2response(chat_id)

        self.assertIn("pollingIntervalMillis", response)
        self.assertIn("nextPageToken", response)
        self.assertIn("items", response)

        logger.debug(json.dumps(response, indent=2))

