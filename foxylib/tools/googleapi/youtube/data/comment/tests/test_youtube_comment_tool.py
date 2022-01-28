import logging
from pprint import pprint
from unittest import TestCase

import pytest

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.data.comment.youtube_comment_tool import YoutubeCommentTool
from foxylib.tools.googleapi.youtube.data.dataapi_tool import DataapiTool, LiveStreamingData
from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestYoutubeCommentTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    # @pytest.mark.skip(reason="save ")
    def test_01(self):
        # https://www.youtube.com/watch?v=CxRIcOLLWZk
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        video_id = 'd3N6JHRt9hc'  # 2021 entertainment top 10
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        youtube_service = YoutubeapiTool.credentials2service(credentials)
        hdocs_comment = YoutubeCommentTool.video_id2hdocs(video_id, youtube_service)

        hdoc_comment = IterTool.iter2singleton_or_none(hdocs_comment)
        pprint(hdoc_comment)

        self.assertEqual(hdoc_comment.get('id'), 'UgyW5jg42_usYEOHd-94AaABAg')


"""
{
    'etag': 'Qn1-IaFHEPiVpnONbLrkY5tIAbI',
    'id': 'UgyW5jg42_usYEOHd-94AaABAg',
    'kind': 'youtube#commentThread',
    'snippet': {
        'canReply': True,
        'isPublic': True,
        'topLevelComment': {
            'etag': 'FHJrKs33PWp44Xv4M98sWnyK60k',
            'id': 'UgyW5jg42_usYEOHd-94AaABAg',
            'kind': 'youtube#comment',
            'snippet': {
                'authorChannelId': {'value': 'UCS_ps6EwQZNyuBKhI5nWFOA'},
                'authorChannelUrl': 'http://www.youtube.com/channel/UCS_ps6EwQZNyuBKhI5nWFOA',
                'authorDisplayName': 'Moonyoung Kang',
                'authorProfileImageUrl': 'https://yt3.ggpht.com/ytc/AKedOLQ2pErc1zWVNUYuZn-DyI5DYk2V4Fnr0bDiANq4ig=s48-c-k-c0x00ffffff-no-rj',
                'canRate': True,
                'likeCount': 1,
                'publishedAt': '2021-12-07T22:39:05Z',
                'textDisplay': '다른 비디오 보고 왔는데, bgm 잘 뽑은 듯.',
                'textOriginal': '다른 비디오 보고 왔는데, bgm 잘 뽑은 듯.',
                'updatedAt': '2021-12-07T22:39:05Z',
                'videoId': 'd3N6JHRt9hc',
                'viewerRating': 'none'
            }
        },
        'totalReplyCount': 0,
        'videoId': 'd3N6JHRt9hc'
    }
}
 """
