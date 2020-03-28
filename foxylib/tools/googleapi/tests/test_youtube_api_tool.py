import os
from functools import partial
from unittest import TestCase

import googleapiclient.discovery
import googleapiclient.errors
import pytest
from google_auth_oauthlib.flow import InstalledAppFlow

from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.googleapi.foxylib_google_api import FoxylibGoogleapi
from foxylib.tools.googleapi.google_api_tool import CredentialCache, GoogleAPITool
from foxylib.tools.json.json_tool import JsonTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestYoutubeApiTool(TestCase):


    ref = {'kind': 'youtube#videoListResponse',
           'etag': '"SJZWTG6xR0eGuCOh2bX6w3s4F94/f5cbsfBnp9md8Drdma3xrVJlFrw"',
           'pageInfo':
               {'totalResults': 1,
                'resultsPerPage': 1
                },
           'items': [
               {'kind': 'youtube#video',
                'etag': '"SJZWTG6xR0eGuCOh2bX6w3s4F94/07l2bBf_ECCx-TclS5Z_62WdbA4"',
                'id': '4VYAaLh3XZg',
                'snippet':
                    {'publishedAt': '2019-12-13T06:20:58.000Z',
                     'channelId': 'UCIZ-JmGTFFDg-5Xlf2SfiVA',
                     'title': '2018년 대한민국 영화 누적 관객수 순위',
                     'description': '2018년 대한민국에서 개봉한 영화들의\n누적 관객수 순위입니다',
                     'thumbnails':
                         {
                             'default': {'url': 'https://i.ytimg.com/vi/4VYAaLh3XZg/default.jpg',
                                         'width': 120,
                                         'height': 90},
                             'medium': {'url': 'https://i.ytimg.com/vi/4VYAaLh3XZg/mqdefault.jpg',
                                        'width': 320,
                                        'height': 180},
                             'high': {'url': 'https://i.ytimg.com/vi/4VYAaLh3XZg/hqdefault.jpg',
                                      'width': 480,
                                      'height': 360},
                             'standard': {'url': 'https://i.ytimg.com/vi/4VYAaLh3XZg/sddefault.jpg',
                                          'width': 640,
                                          'height': 480}
                         },
                     'channelTitle': 'Foxytrixy the datamage',
                     'categoryId': '25',
                     'liveBroadcastContent': 'none',
                     'localized': {'title': '2018년 대한민국 영화 누적 관객수 순위',
                                   'description': '2018년 대한민국에서 개봉한 영화들의\n누적 관객수 순위입니다'},
                     'defaultAudioLanguage': 'ko'},
                'contentDetails': {'duration': 'PT2M4S',
                                   'dimension': '2d',
                                   'definition': 'hd',
                                   'caption': 'false',
                                   'licensedContent': False,
                                   'projection': 'rectangular',
                                   'hasCustomThumbnail': True},
                'statistics': {'viewCount': '27',
                               'likeCount': '0',
                               'dislikeCount': '0',
                               'favoriteCount': '0',
                               'commentCount': '0'}}]}


    @pytest.mark.skip(reason="involve human interaction")
    def test_01(self):
        youtube_id = "4VYAaLh3XZg"

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


        cachefile = os.path.join(FILE_DIR, "token.pickle")
        cachefuncs = CredentialCache.filepath2cachefuncs_pickle(cachefile)

        flow = InstalledAppFlow.from_client_secrets_file(FoxylibGoogleapi.Oauth.filepath_credentials(), scopes)
        credentials = GoogleAPITool.cache_or_func2cred(cachefuncs, partial(flow.run_local_server, port=0))

        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=youtube_id
        )
        response = request.execute()


        hyp_01 = JsonTool.down(response, ["kind"])
        self.assertEqual(hyp_01, "youtube#videoListResponse")

        item = l_singleton2obj(JsonTool.down(response, ["items"]))

        hyp_02 = JsonTool.down(item, ["id"])
        self.assertEqual(hyp_02, youtube_id)

        hyp_03 = JsonTool.down(item, ["kind"])
        self.assertEqual(hyp_03, "youtube#video")


    # def test_05(self):
    #     video_id_private = "QBT-3wkPetU"
    #     # url_private = "https://www.youtube.com/watch?v=QBT-3wkPetU"
    #
    #     # -*- coding: utf-8 -*-
    #
    #     # Sample Python code for youtube.videos.list
    #     # See instructions for running these code samples locally:
    #     # https://developers.google.com/explorer-help/guides/code_samples#python
    #
    #     import os
    #
    #     import google_auth_oauthlib.flow
    #     import googleapiclient.discovery
    #     import googleapiclient.errors
    #
    #     scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    #
    #     def main():
    #         # Disable OAuthlib's HTTPS verification when running locally.
    #         # *DO NOT* leave this option enabled in production.
    #         os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    #
    #         api_service_name = "youtube"
    #         api_version = "v3"
    #         client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    #
    #         # Get credentials and create an API client
    #         flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #             client_secrets_file, scopes)
    #         credentials = flow.run_console()
    #         youtube = googleapiclient.discovery.build(
    #             api_service_name, api_version, credentials=credentials)
    #
    #         request = youtube.videos().list(
    #             part="status",
    #             id="QBT-3wkPetU"
    #         )
    #         response = request.execute()
    #
    #         print(response)
