import logging

import requests
from nose.tools import assert_true
from slack import WebClient, RTMClient

from foxylib.hub.logger.foxylib_logger import FoxylibLogger
from foxylib.tools.bytes.bytes_tool import BytesTool
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool
from foxylib.tools.http.http_tool import HttpTool, HttprTool
from foxylib.tools.json.json_tool import jdown
from foxylib.tools.string.string_tool import str2strip, str2lower


class SlackTool:
    PRIVATE_URI_PREFIX = "https://files.slack.com/files-pri/"

    @classmethod
    def token2rtm_client(cls, xoxb_token):
        return RTMClient(token=xoxb_token)

    @classmethod
    def token2web_client(cls, xoxb_token):
        return WebClient(token=xoxb_token)

    @classmethod
    def token2headers(cls, xoxp_token):
        return {"Authorization": "Bearer {}".format(xoxp_token),}

    @classmethod
    def fileurl_token2bytes(cls, url, xoxp_token):
        logger = FoxylibLogger.func_level2logger(cls.fileurl_token2bytes, logging.DEBUG)

        headers = cls.token2headers(xoxp_token)
        httpr = requests.get(url, headers=headers)

        curl = HttprTool.request2curl(httpr.request)
        logger.debug({"curl":curl})

        assert(httpr.ok)

        return httpr.content

    @classmethod
    def fileurl_token2utf8(cls, *_, **__):
        bytes = cls.fileurl_token2bytes(*_, **__)
        return BytesTool.bytes2utf8(bytes)

    @classmethod
    def fileurl_token2file(cls, url, xoxp_token, filepath,):
        bytes = cls.fileurl_token2bytes(url, xoxp_token)
        FileTool.bytes2file(bytes, filepath)


    @classmethod
    def str2j_block_list(cls, str_in):
        l = str_in.splitlines()
        n = len(l)
        p = 20
        k = n // p + (1 if n % p else 0)

        j_list = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(l[i * p:(i + 1) * p]),
            },
        } for i in range(k)]
        return j_list

    @classmethod
    def j_blocks2h_msg(cls, channel, username, j_blocks):
        h = {
            "channel": channel,
            "username": username,
            "blocks": j_blocks,
        }
        return h

    @classmethod
    def h_payload2text(cls, h): return h["data"].get("text")

    @classmethod
    def h_payload2channel(cls, h): return h["data"].get("channel")

    @classmethod
    def h_payload2web_client(cls, h): return h["web_client"]

    @classmethod
    def str_in2str_cmd_body(cls, str_in):
        str_clean = str2lower(str2strip(str_in))
        if not str_clean: return None

        l = str_clean.split(maxsplit=1)
        assert_true(l)

        str_cmd = l[0]
        str_body = l[1] if len(l)>1 else None
        return (str_cmd, str_body,)

class SlackFiletype:
    class Value:
        PYTHON = "python"
        TEXT = "text"
    V = Value

    @classmethod
    def mimetype2filetype(cls, mimetype):
        h = {MimetypeTool.V.TEXT_XPYTHON:cls.V.PYTHON,
             MimetypeTool.V.TEXT_PLAIN:cls.V.TEXT,
             }

        return h.get(mimetype)

class SlackFileUpload:
    @classmethod
    def j_response2j_file(cls, j_response):
        return j_response.get("file")

    @classmethod
    def j_response2mimetype(cls, j_response):
        return jdown(j_response, ["file", "mimetype"])

    @classmethod
    def j_response2file_id(cls, j_response):
        return jdown(j_response, ["file","id"])


    @classmethod
    def j_file2id(cls, j_file):
        return j_file.get("id")

    @classmethod
    def j_file2mimetype(cls, j_file):
        return j_file.get("mimetype")

    @classmethod
    def j_file2url_private(cls, j_file):
        return j_file.get("url_private")
