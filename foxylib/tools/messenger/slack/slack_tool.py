import copy
import json
import logging
import os
from typing import Callable

import requests
from future.utils import lmap
from nose.tools import assert_true
from slack import WebClient, RTMClient

from foxylib.tools.collections.collections_tool import list2singleton, l_singleton2obj
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.bytes.bytes_tool import BytesTool
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool
from foxylib.tools.http.http_tool import HttpTool, HttprTool
from foxylib.tools.json.json_tool import jdown, JsonTool
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




    @classmethod
    def client_file_id2files_delete(cls, web_client, file_id):
        response = web_client.files_delete(**{"file": file_id})
        return response

    @classmethod
    def add_listener2rtm_client(cls, rtm_client, *, event: str, callback: Callable):
        # reference: RTMClient.on

        if isinstance(callback, list):
            for cb in callback:
                RTMClient._validate_callback(cb)
            previous_callbacks = rtm_client._callbacks[event]
            RTMClient._callbacks[event] = list(set(previous_callbacks + callback))
        else:
            RTMClient._validate_callback(callback)
            rtm_client._callbacks[event].append(callback)


    @classmethod
    def rtm_client2event_loop(cls, rtm_client):
        return rtm_client._event_loop

class FileUploadMethod:
    @classmethod
    def j_response2norm(cls, j_response):
        jpath_list_exclusive = lmap(lambda s: s.split("."),
                                   ["file.id",
                                    "file.created",
                                    "file.timestamp",
                                    "file.url_private",
                                    "file.url_private_download",
                                    "file.permalink",
                                    "file.permalink_public",
                                    "file.edit_link",
                                    "file.preview",
                                    "file.preview_highlight",
                                    "file.shares.public",
                                    ])

        return JsonTool.j_jpaths2excluded(j_response, jpath_list_exclusive)



class SlackEvent:
    @classmethod
    def j2client_msg_id(cls, j_event):
        return j_event["client_msg_id"]

    @classmethod
    def j2plaintext(cls, j_event):
        # https://api.slack.com/changelog/2019-09-what-they-see-is-what-you-get-and-more-and-less

        j_rich_text_list = j_event.get("blocks")
        if not j_rich_text_list:
            return None

        j_rich_text = l_singleton2obj(j_rich_text_list)
        j_rich_text_section_list = j_rich_text.get("elements")
        if not j_rich_text_section_list:
            return None

        j_rich_text_section = l_singleton2obj(j_rich_text_section_list)
        j_element_list = j_rich_text_section.get("elements")
        if not j_element_list:
            return None

        text_list = lmap(lambda j:j["text"], filter(lambda j:j["type"]=="text", j_element_list))
        return "".join(text_list)

    @classmethod
    def j2user(cls, j_event):
        return j_event.get("user")


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

class SlackFile:
    @classmethod
    def j_file2id(cls, j_file):
        return j_file.get("id")

    @classmethod
    def j_file2mimetype(cls, j_file):
        return j_file.get("mimetype")

    @classmethod
    def j_file2url_private(cls, j_file):
        return j_file.get("url_private")

    @classmethod
    def j_file2user_id(cls, j_file):
        return j_file.get("user")

    @classmethod
    def j_file2filename(cls, j_file):
        return j_file.get("name")

    @classmethod
    def j_file2title(cls, j_file):
        return j_file.get("title")
