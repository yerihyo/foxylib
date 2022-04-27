import logging
import os
from functools import partial
from pprint import pprint
from unittest import TestCase

import pytest

from foxylib.tools.cache.cache_tool import CacheTool
from foxylib.tools.collections.collections_tool import lchain
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.data.comment.youtube_commentthread_tool import YoutubeCommentthreadTool
from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.readwriter.file.file_readwriter import FileReadwriterTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestYoutubeCommentthreadTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="WORKING. Uses token")
    def test_01(self):
        # https://www.youtube.com/watch?v=CxRIcOLLWZk
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        video_id = 'd3N6JHRt9hc'  # 2021 entertainment top 10
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        youtube_service = YoutubeapiTool.credentials2service(credentials)
        hdocs_comment = YoutubeCommentthreadTool.video_id2items(video_id, youtube_service)

        pprint({
            'hdocs_comment': list(hdocs_comment),
        })

        # hdoc_comment = IterTool.iter2singleton_or_none(hdocs_comment)
        # pprint(hdoc_comment)
        #
        # self.assertEqual(hdoc_comment.get('id'), 'UgyW5jg42_usYEOHd-94AaABAg')

    @pytest.mark.skip(reason="WORKING. Uses token")
    def test_02(self):
        # https://www.youtube.com/watch?v=CxRIcOLLWZk
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        # video_id = 'd3N6JHRt9hc'  # 2021 entertainment top 10
        video_id = '1lGo3pzxHDc'  # iron fertilization

        filepath_commentthreads = os.path.join(FILE_DIR, 'tmp', f'{video_id}.commentthreads.yaml')
        @partial(
            CacheTool.func2readwriter_wrapped,
            readwriter=FileReadwriterTool.filepath2yaml_readwriter(filepath_commentthreads),
        )
        def video_id2hdocs_commentthread(video_id):
            credentials = FoxylibGoogleapi.ServiceAccount.credentials()
            youtube_service = YoutubeapiTool.credentials2service(credentials)
            return list(
                YoutubeCommentthreadTool.video_id2items(video_id, youtube_service)
            )

        filepath_comments = os.path.join(FILE_DIR, 'tmp', f'{video_id}.comments.yaml')
        @partial(
            CacheTool.func2readwriter_wrapped,
            readwriter=FileReadwriterTool.filepath2yaml_readwriter(filepath_comments),
        )
        def video_id2hdocs_comment(video_id):
            hdocs_commentthread = video_id2hdocs_commentthread(video_id)

            hdocs_comment_raw = lchain(
                *map(YoutubeCommentthreadTool.hdoc_commentthread2hdocs, hdocs_commentthread)
            )
            # hdocs_comment_raw = [
            #     hdoc_comment
            #     for hdoc_commentthread in hdocs_commentthread
            #     for hdoc_comment in YoutubeCommentthreadTool.hdoc_commentthread2hdocs(hdoc_commentthread)
            # ]
            hdocs_comment = sorted(
                hdocs_comment_raw,
                key=YoutubeCommentthreadTool.hdoc2publishedAt,
            )
            return [{
                'key': f"YOUTUBE/{hdoc_comment['id']}",
                'body': hdoc_comment,
                'source': {'media': "YOUTUBE", 'id': hdoc_comment['id'], },
                # 'value': 'SUPPORT',
            } for hdoc_comment in hdocs_comment]

        hdocs_comment = video_id2hdocs_comment(video_id)

        filepath_annotations = os.path.join(FILE_DIR, 'tmp', f'{video_id}.annotations.csv')
        @partial(
            CacheTool.func2readwriter_wrapped,
            readwriter=FileReadwriterTool.filepath2csv_readwriter(filepath_annotations),
        )
        def hdoc_comments2hdoc_annotations(hdocs_comment):
            return [(
                hdoc_comment.get('key'),
                JsonTool.down(hdoc_comment, ['body', 'snippet', 'authorDisplayName']),
                JsonTool.down(hdoc_comment, ['body', 'snippet', 'textOriginal']),
            )
                for hdoc_comment in hdocs_comment]

        hdoc_comments2hdoc_annotations(hdocs_comment)


        logger.debug({
            'len(hdocs_comment)': len(hdocs_comment),
            # 'len(hdocs_commentthread)': len(hdocs_commentthread),
        })

        # self.assertEqual(hdoc_comment.get('id'), 'UgyW5jg42_usYEOHd-94AaABAg')


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
