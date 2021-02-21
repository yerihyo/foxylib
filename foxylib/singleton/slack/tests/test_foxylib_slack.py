import asyncio
import concurrent.futures
import json
import logging
import os
import time
from datetime import datetime
from functools import partial
from pprint import pprint
from unittest import TestCase

import pytest
import requests
from slack import RTMClient

from foxylib.singleton.slack.foxylib_slack import FoxylibSlack, FoxylibChannel
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.messenger.slack.methods.files.upload import FilesUploadMethod
from foxylib.tools.messenger.slack.methods.response_tool import SlackResponseTool
from foxylib.tools.messenger.slack.slack_tool import SlackFile, SlackTool, FileUploadMethod

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)



class TestFoxylibSlack(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="Auth error when running from travis CI")
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        web_client = FoxylibSlack.web_client()
        channel = FoxylibChannel.V.FOXYLIB
        filepath = os.path.join(FILE_DIR, "test_01.txt")
        response = FilesUploadMethod.invoke(web_client, channel, filepath)
        self.assertTrue(SlackResponseTool.response2is_ok(response))

        j_response = SlackResponseTool.response2j_resopnse(response)
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
                "channel": [
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
        j_file = FilesUploadMethod.j_response2j_file(j_response)
        file_id = SlackFile.j_file2id(j_file)
        web_client.files_delete(**{"file": file_id})

    @pytest.mark.skip(reason="Auth error when running from travis CI")
    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        web_client = FoxylibSlack.web_client()
        channel = FoxylibChannel.V.FOXYLIB
        filepath = os.path.join(FILE_DIR, "test_01.txt")
        response = FilesUploadMethod.invoke(web_client, channel, filepath)
        self.assertTrue(SlackResponseTool.response2is_ok(response))

        j_response = SlackResponseTool.response2j_resopnse(response)
        j_file = FilesUploadMethod.j_response2j_file(j_response)
        logger.debug(json.dumps({"j_file":j_file}, indent=2))
        self.assertEqual(SlackFile.j_file2mimetype(j_file), MimetypeTool.V.TEXT_PLAIN)

        # download
        url_private = SlackFile.j_file2url_private(j_file)
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
        file_id = SlackFile.j_file2id(j_file)
        web_client.files_delete(**{"file":file_id})


    @pytest.mark.skip(reason="RTM not receiving message event yet")
    def test_03(self):
        @RTMClient.run_on(event='message')
        def say_hello(**payload):
            # raise Exception("adfadf")
            data = payload['data']
            print(data.get('text'))


        def sync_loop(rtm_client):
            web_client = FoxylibSlack.web_client()
            for i in range(3):
                time.sleep(1)

                # raise Exception(list(rtm_client._callbacks.keys()))

                msg = "Hi there: #{} @ {}".format(i+1, datetime.now())
                # web_client.chat_postMessage(channel=FoxylibChannel.V.FOXYLIB, text=msg)
                print("Hi there: #{} @ {}".format(i+1, datetime.now()))

            rtm_client.stop()

        async def slack_main():
            loop = asyncio.get_event_loop()
            rtm_client = RTMClient(token=FoxylibSlack.xoxb_token(), run_async=True, loop=loop)

            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            await asyncio.gather(
                loop.run_in_executor(executor, partial(sync_loop, rtm_client)),
                rtm_client.start()
            )
            # rtm_client.stop()


        asyncio.run(slack_main())

    def test_04(self):
        logger = FoxylibLogger.func_level2logger(self.test_04, logging.DEBUG)

        channel = "C014DTPM24V"
        headers = {"Content-type": 'application/json',
                   "Authorization": "Bearer {}".format(FoxylibSlack.xoxb_token()),
                   }
        json1 = {"channel": channel,
             "text": "Hello world :tada:",
             }

        response1 = requests.post("https://slack.com/api/chat.postMessage",
                                 headers=headers,
                                 json=json1)

        self.assertEqual(response1.status_code, requests.codes.ok)

        j1 = response1.json()
        self.assertTrue(j1.get("ok"), j1)

        ts = JsonTool.down(j1, ["message", "ts"])
        json2 = {"channel": channel,
             "ts": ts,
             }

        response2 = requests.post("https://slack.com/api/chat.delete",
                                 headers=headers,
                                 json=json2)

        self.assertEqual(response2.status_code, requests.codes.ok)

        j2 = response2.json()
        self.assertTrue(j2.get("ok"), j2)




