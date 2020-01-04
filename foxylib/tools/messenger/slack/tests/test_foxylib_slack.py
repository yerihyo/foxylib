import json
import logging
import os
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.messenger.slack.foxylib_slack import FoxylibSlack, FoxylibChannel
from foxylib.tools.messenger.slack.slack_tool import SlackFiletype, SlackFileUpload, SlackTool, FileUploadMethod
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

        j_response = SlackTool.response2j_resopnse(response)
        hyp = j_response
        ref = {
            "ok": True,
            "file": {
                # "id": "FSB2C7L4F",
                # "created": 1578114293,
                # "timestamp": 1578114293,
                "name": "test_01.txt",
                "title": "test 01",
                "mimetype": "text/plain",
                "filetype": "text",
                "pretty_type": "Plain Text",
                "user": "US8SU4H8W",
                "editable": True,
                "size": 30,
                "mode": "snippet",
                "is_external": False,
                "external_type": "",
                "is_public": True,
                "public_url_shared": False,
                "display_as_bot": False,
                "username": "",
                # "url_private": "https://files.slack.com/files-pri/TB2V2S5L6-FSB2C7L4F/test_01.txt",
                # "url_private_download": "https://files.slack.com/files-pri/TB2V2S5L6-FSB2C7L4F/download/test_01.txt",
                # "permalink": "https://foxytrixy.slack.com/files/US8SU4H8W/FSB2C7L4F/test_01.txt",
                # "permalink_public": "https://slack-files.com/TB2V2S5L6-FSB2C7L4F-1846b53c2e",
                # "edit_link": "https://foxytrixy.slack.com/files/US8SU4H8W/FSB2C7L4F/test_01.txt/edit",
                # "preview": "\ud14c\uc2a4\ud2b8\uc6a9 \ud30c\uc77c\n\u314e\u314e\u314e\n",
                # "preview_highlight": "<div class=\"CodeMirror cm-s-default CodeMirrorServer\" oncopy=\"if(event.clipboardData){event.clipboardData.setData('text/plain',window.getSelection().toString().replace(/\\u200b/g,''));event.preventDefault();event.stopPropagation();}\">\n<div class=\"CodeMirror-code\">\n<div><pre>\ud14c\uc2a4\ud2b8\uc6a9 \ud30c\uc77c</pre></div>\n<div><pre>\u314e\u314e\u314e</pre></div>\n<div><pre></pre></div>\n</div>\n</div>\n",
                "lines": 3,
                "lines_more": 0,
                "preview_is_truncated": False,
                "comments_count": 0,
                "is_starred": False,
                "shares": {
                    # "public": {
                    #     "CS7V80KGE": [
                    #         {
                    #             "reply_users": [],
                    #             "reply_users_count": 0,
                    #             "reply_count": 0,
                    #             "ts": "1578114293.000400",
                    #             "channel_name": "foxylib",
                    #             "team_id": "TB2V2S5L6"
                    #         }
                    #     ]
                    # }
                },
                "channels": [
                    "CS7V80KGE"
                ],
                "groups": [],
                "ims": [],
                "has_rich_preview": False
            }
        }
        # logger.debug(json.dumps({"j_response":j_response}, indent=2))
        self.assertEqual(FileUploadMethod.j_response2norm(hyp), ref)

        # cleanup
        file_id = SlackFileUpload.j_response2file_id(j_response)
        web_client.files_delete(**{"file": file_id})



    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

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
