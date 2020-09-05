# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

from foxylib.tools.collections.collections_tool import l_singleton2obj


from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool


# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

class LiveStreamingData:
    @classmethod
    def data2chat_id(cls, data):
        return data["activeLiveChatId"]

class DataapiTool:
    @classmethod
    def video_id2live_streaming_data(cls, video_id):
        # https://stackoverflow.com/questions/36683878/youtube-api-how-do-i-get-the-livechatid
        # https://developers.google.com/youtube/v3/docs/videos/list

        from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi

        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        service = YoutubeapiTool.credentials2service(credentials)
        request = service.videos().list(id=video_id, part='liveStreamingDetails',)
        response = request.execute()

        items = response.get("items")
        if not items:
            return None

        item = l_singleton2obj(items)

        return item.get("liveStreamingDetails")

