import logging
import os
import pickle
from functools import reduce, partial, lru_cache

from foxylib.tools.googleapi.youtube.data.dataapi_tool import DataapiTool, LiveStreamingData
from foxylib.tools.googleapi.youtube.livestreaming.livestreamingapi_tool import LiveChatMessagesTool
from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.oauth.oauth2_tool import OAuth2Tool
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.readwriter.pickle_readwriter import PickleReadwriter
from foxylib.tools.googleapi.googleapi_tool import GoogleapiTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)


class FoxylibGoogleapi:

    class OAuth:
        @classmethod
        def filepath_credentials(cls):
            return os.path.join(REPO_DIR, "env", "googleapi", "foxylib.foxylib-test.clientid.credential.json")


        @classmethod
        def scopes2credentials_flow(cls, scopes):
            # Get credentials and create an API client
            # scopes = ["https://www.googleapis.com/auth/youtube"]
            client_secrets_file = cls.filepath_credentials()
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            return flow

        @classmethod
        def gereate_credentials(cls, scopes, flow2credentials, filepath):
            flow = cls.scopes2credentials_flow(scopes)
            f_create = partial(flow2credentials, flow)

            refresh_credentials = GoogleapiTool.credentials2refreshed
            readwriter = PickleReadwriter(filepath)
            credentials = OAuth2Tool.gereate_credentials(f_create, refresh_credentials, readwriter)
            return credentials

    class ServiceAccount:
        @classmethod
        def filepath_privatekey(cls):
            # http://console.cloud.google.com/iam-admin/serviceaccounts/details/112472142364049649520
            return os.path.join(REPO_DIR, "env", "googleapi", "foxylib-ff3a87675bbe.json")

        @classmethod
        def credentials(cls):
            # https://developers.google.com/identity/protocols/oauth2/service-account
            # https://cloud.google.com/docs/authentication/
            return Credentials.from_service_account_file(cls.filepath_privatekey())


class FoxytrixyYoutubelive:
    @classmethod
    def filepath_token_youtube(cls):
        return os.path.join(FILE_DIR, "token", "original", "foxylib.foxylib-test.clientid.youtube.token.pickle")

    @classmethod
    def video_id(cls):
        return "RtpYrpXGEjA"

    @classmethod
    @lru_cache(maxsize=2)
    def live_chat_id(cls):
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        data = DataapiTool.video_id2live_streaming_data(cls.video_id(), credentials)
        live_chat_id = LiveStreamingData.data2chat_id(data)
        return live_chat_id

    @classmethod
    def service_oath(cls):
        scopes = ["https://www.googleapis.com/auth/youtube"]
        filepath_token = cls.filepath_token_youtube()
        credentials = FoxylibGoogleapi.OAuth.gereate_credentials(scopes, lambda f: f.run_console(), filepath_token)
        service = YoutubeapiTool.credentials2service(credentials)
        return service

    @classmethod
    def text2livechat(cls, text):
        logger = FoxylibLogger.func_level2logger(cls.text2livechat, logging.DEBUG)
        """
        example
        
        {'kind': 'youtube#liveChatMessage', 'etag': 'Owg4Et-BphpBk9yhBsHVOdsU7QQ',
         'id': 'LCC.CjgKDQoLUnRwWXJwWEdFakEqJwoYVUNJWi1KbUdURkZEZy01WGxmMlNmaVZBEgtSdHBZcnBYR0VqQRIcChpDTDduNi03bDBPc0NGV05EN1FvZFk2QU1WUQ',
         'snippet': {'type': 'textMessageEvent',
                     'liveChatId': 'Cg0KC1J0cFlycFhHRWpBKicKGFVDSVotSm1HVEZGRGctNVhsZjJTZmlWQRILUnRwWXJwWEdFakE',
                     'authorChannelId': 'UCIZ-JmGTFFDg-5Xlf2SfiVA', 'publishedAt': '2020-09-05T00:50:07.034000Z',
                     'hasDisplayContent': True, 'displayMessage': 'hello world',
                     'textMessageDetails': {'messageText': 'hello world'}}}
                     """

        return LiveChatMessagesTool.text2chat(cls.service_oath(), cls.live_chat_id(), text)
