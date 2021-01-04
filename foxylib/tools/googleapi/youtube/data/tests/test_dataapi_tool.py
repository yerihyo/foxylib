import logging
from unittest import TestCase

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.data.dataapi_tool import DataapiTool, LiveStreamingData
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDataapiTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        # https://www.youtube.com/watch?v=nHRKoNOQ56w
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        video_id = 'nHRKoNOQ56w'
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        data = DataapiTool.video_id2live_streaming_data(video_id, credentials)
        chat_id = LiveStreamingData.data2chat_id(data)

        ref = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'
        self.assertEqual(chat_id, ref)

    # ptah-dev
    def test_02(self):
        # https://www.youtube.com/watch?v=CxRIcOLLWZk
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        video_id = 'ePnWBJnj7C0'
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        data = DataapiTool.video_id2live_streaming_data(video_id, credentials)
        chat_id = LiveStreamingData.data2chat_id(data)

        # logger.debug({'chat_id':chat_id})
        # ref = 'Cg0KC0N4UkljT0xMV1prKicKGFVDTDI5X1pkaENHV3pjMTZ1NW04S19VURILQ3hSSWNPTExXWms'
        ref = 'Cg0KC2VQbldCSm5qN0MwKicKGFVDTDI5X1pkaENHV3pjMTZ1NW04S19VURILZVBuV0JKbmo3QzA'
        self.assertEqual(chat_id, ref)

