import json
import logging
import os
from unittest import TestCase

from foxylib.hub.logger.foxylib_logger import FoxylibLogger
from foxylib.hub.messenger.slack.foxylib_slack import FoxylibChannel, FoxylibSlack
from foxylib.tools.messenger.slack.slack_tool import SlackFiletype, SlackFileUpload, SlackTool
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestFoxylibSlack(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        web_client = FoxylibSlack.web_client()
        channel = FoxylibChannel.V.FOXYLIB
        filepath = os.path.join(FILE_DIR, "test_01.txt")
        response = SlackTool.client_channel_filepath2files_upload(web_client, channel, filepath)
        self.assertTrue(SlackTool.response2is_ok(response))

        j_file = SlackFileUpload.j_response2j_file(SlackTool.response2j_resopnse(response))
        logger.debug(json.dumps({"j_file":j_file}, indent=2))
        self.assertEqual(SlackFileUpload.j_file2mimetype(j_file), MimetypeTool.V.TEXT_PLAIN)

        # download
        url_private = SlackFileUpload.j_file2url_private(j_file)
        self.assertEqual(MimetypeTool.url2mimetype(url_private), MimetypeTool.V.TEXT_PLAIN)

        token = FoxylibSlack.xoxp_token()
        logger.debug({"url_private":url_private,
                      "token":token,
                      })
        utf8 = SlackTool.fileurl_token2utf8(url_private, token)
        logger.debug({"utf8": utf8})
        # FileTool.utf82file(utf8, "/tmp/t.html")
        self.assertEqual(utf8, FileTool.filepath2utf8(filepath))




        # cleanup
        file_id = SlackFileUpload.j_response2file_id(response.data)
        web_client.files_delete(**{"file":file_id})
