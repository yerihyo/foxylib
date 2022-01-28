# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import logging
from functools import lru_cache
from typing import Optional, Iterable

from foxylib.tools.collections.collections_tool import l_singleton2obj


from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool


# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class LiveStreamingData:
    @classmethod
    def data2chat_id(cls, data):
        if not data:
            return None

        return data.get("activeLiveChatId")


class DataapiTool:
    class Sample:
        @classmethod
        @lru_cache(maxsize=1)
        def video_id(cls):
            return '7sbNO9VlSFM'  # sciencetackle / sealevelrise

    @classmethod
    def video_id2live_streaming_data(cls, video_id, service) -> Optional[dict]:
        logger = FoxylibLogger.func_level2logger(cls.video_id2live_streaming_data, logging.DEBUG)

        # https://stackoverflow.com/questions/36683878/youtube-api-how-do-i-get-the-livechatid
        # https://developers.google.com/youtube/v3/docs/videos/list

        # credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        # service = YoutubeapiTool.credentials2service(credentials)
        # if not video_id:
        #     return None

        request = service.videos().list(id=video_id, part='liveStreamingDetails',)
        response = request.execute()

        logger.debug({"response":response})

        items = response.get("items")
        if not items:
            return None

        item = l_singleton2obj(items)

        return item.get("liveStreamingDetails")

