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


        filepath = os.path.join(FILE_DIR, "test_01.txt")
        mimetype = FileTool.filepath2mimetype(filepath)
        filetype = SlackFiletype.mimetype2filetype(mimetype)

        j_files_upload_in = {"channels": FoxylibChannel.V.FOXYLIB,
                             "file": filepath,
                             "filename": os.path.basename(filepath),
                             "filetype": filetype,
                             }

        web_client = FoxylibSlack.web_client()

        # upload
        response = web_client.files_upload(**j_files_upload_in)
        logger.debug({"response.data":response.data})

        j_file = SlackFileUpload.j_response2j_file(response.data)
        self.assertEqual(SlackFileUpload.j_file2mimetype(j_file), MimetypeTool.V.TEXT_PLAIN)
        self.assertTrue(response["ok"])


        # download
        url_private = SlackFileUpload.j_file2url_private(j_file)
        self.assertEqual(MimetypeTool.url2mimetype(url_private), MimetypeTool.V.TEXT_PLAIN)

        utf8 = SlackTool.fileurl_token2utf8(url_private, FoxylibSlack.xoxp_token())
        logger.debug({"utf8": utf8})
        # FileTool.utf82file(utf8, "/tmp/t.html")
        self.assertEqual(utf8, FileTool.filepath2utf8(filepath))




        # cleanup
        file_id = SlackFileUpload.j_response2file_id(response.data)
        web_client.files_delete(**{"file":file_id})
