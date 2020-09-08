# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import logging
import os
from datetime import datetime, timedelta

import googleapiclient.discovery
import googleapiclient.errors
import pytz


from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.json.json_tool import JsonTool

# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


# class LiveStreamsTool:
#     @classmethod
#     def body2response(cls, credentials, body):
#         service = YoutubeapiTool.credentials2service(credentials)
#
#         request = service.liveStreams().insert(
#             part="snippet,cdn,contentDetails,status",
#             body=body
#
#         )
#         response = request.execute()
#         return response
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class LiveChatMessagesTool:
    @classmethod
    def list(cls, credentials, live_chat_id):
        service = YoutubeapiTool.credentials2service(credentials)

        request = service.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="id,snippet,authorDetails"
        )
        response = request.execute()
        return response

    @classmethod
    def response2items(cls, response):
        return response.get("items") or []

    @classmethod
    def item2id(cls, item):
        return item["id"]

    @classmethod
    def item2message(cls, item):
        msg = JsonTool.down(item, ["snippet","textMessageDetails","messageText"])
        return msg

    @classmethod
    def response2pollingIntervalMillis(cls, response):
        return response['pollingIntervalMillis']

    @classmethod
    def response2datetime_next_poll(cls, response):
        polling_interval_millis = cls.response2pollingIntervalMillis(response)
        dt_now = datetime.now(pytz.utc)
        return dt_now + timedelta(milliseconds=polling_interval_millis)

    @classmethod
    def text2body_insert(cls, live_chat_id, text):
        body = {
            "snippet": {
                "liveChatId": live_chat_id,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": text,
                }
            }
        }
        return body

    @classmethod
    def text2chat(cls, service, live_chat_id, text):
        body = LiveChatMessagesTool.text2body_insert(live_chat_id, text)
        request = service.liveChatMessages().insert(part="snippet", body=body)
        response = request.execute()
        return response


def main():
    # https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list?apix=true

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # api_service_name = "youtube"
    # api_version = "v3"
    # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
    credentials = FoxylibGoogleapi.ServiceAccount.credentials()
    service = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials, cache_discovery=False)


    chat_id = 'Cg0KC25IUktvTk9RNTZ3KicKGFVDbXJscUZJS19RUUNzcjNGUkhhM09LdxILbkhSS29OT1E1Nnc'

    request = service.liveChatMessages().list(
        liveChatId=chat_id,
        part="id,snippet,authorDetails"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
