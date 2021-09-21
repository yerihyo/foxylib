# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import logging
import os
from datetime import timedelta
from decimal import Decimal

import googleapiclient.discovery
import googleapiclient.errors
import dateutil.parser

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.finance.forex.forex_tool import Forex
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


class Response:
    class Field:
        nextPageToken = "nextPageToken"
        items = "items"
        pollingIntervalMillis = "pollingIntervalMillis"

    @classmethod
    def response2pollingIntervalMillis(cls, response):
        return response[Response.Field.pollingIntervalMillis]

    @classmethod
    def response2dt_next_poll(cls, response, dt_now):
        polling_interval_millis = cls.response2pollingIntervalMillis(response)
        # dt_now = datetime.now(pytz.utc)
        return dt_now + timedelta(milliseconds=polling_interval_millis)

    @classmethod
    def response2items(cls, response):
        return response.get(Response.Field.items) or []


class LiveChatMessagesTool:
    @classmethod
    def list(cls, credentials, live_chat_id, page_token=None):
        service = YoutubeapiTool.credentials2service(credentials)

        kwargs = {"liveChatId": live_chat_id,
                  "part": "id,snippet,authorDetails",
                  "pageToken": page_token,
                  }
        request = service.liveChatMessages().list(
            **DictTool.filter(lambda k, v: v, kwargs)
        )
        try:
            response = request.execute()
        except googleapiclient.errors.HttpError as e:
            if e.resp.status == 403:
                return None
            raise

        return response

    @classmethod
    def item2id(cls, item):
        return item["id"]

    @classmethod
    def item2published_at(cls, item):
        str_raw = JsonTool.down(item, ["snippet", "publishedAt"])
        return dateutil.parser.parse(str_raw)
    #
    # @classmethod
    # def item2super_chat(cls, item):
    #     super_chat = JsonTool.down(item, ["snippet", "superChatDetails", ])
    #     return super_chat

    @classmethod
    def item2super_chat_forex(cls, item):
        logger = FoxylibLogger.func_level2logger(cls.item2super_chat_forex,
                                                 logging.DEBUG)

        jpath_superChatDetails = ["snippet", "superChatDetails"]
        superChatDetails = JsonTool.down(item, jpath_superChatDetails)
        if not superChatDetails:
            return None

        currency = superChatDetails.get("currency")
        amountMicros = superChatDetails["amountMicros"]
        if not amountMicros:
            return None

        # logger.debug({"amountMicros":amountMicros})
        decimal = Decimal(amountMicros) / 1000000

        forex = {Forex.Field.CURRENCY: currency,
                 Forex.Field.DECIMAL: decimal,
                 }

        return forex

    @classmethod
    def item2message(cls, item):
        msg_superchat = JsonTool.down(item, ["snippet", "superChatDetails", "userComment"])
        if msg_superchat:
            return msg_superchat

        msg_normal = JsonTool.down(item, ["snippet", "textMessageDetails", "messageText"])
        return msg_normal


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
    def text2livechat(cls, service, live_chat_id, text):
        logger = FoxylibLogger.func_level2logger(cls.text2livechat, logging.DEBUG)

        body = LiveChatMessagesTool.text2body_insert(live_chat_id, text)
        logger.debug({'body':body,})
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
