import logging
import re
from functools import lru_cache
from pprint import pformat
from unittest import TestCase

import pytest

from foxylib.tools.google.youtube.youtube_tool import YoutubeTool
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.googleapi.youtube.youtubeapi_tool import YoutubeapiTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import MatchTool
from foxylib.tools.url.url_tool import URLTool


class TestYoutubeTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        url = "https://www.youtube.com/watch?v=4VYAaLh3XZg&t=33s"
        hyp = YoutubeTool.url2video_id(url)
        ref = "4VYAaLh3XZg"

        self.assertEqual(hyp, ref)


    def test_02(self):
        video_id = "4VYAaLh3XZg"
        hyp = YoutubeTool.video_id2url(video_id)
        ref = "https://www.youtube.com/watch?v=4VYAaLh3XZg"

        self.assertEqual(hyp, ref)

    def test_03(self):
        url = "https://www.youtube.com/watch?v=4VYAaLh3XZg"
        hyp = URLTool.url2is_accessible(url)

        self.assertTrue(hyp)

    def test_04(self):
        logger = FoxylibLogger.func_level2logger(self.test_04, logging.DEBUG)

        # https://stackoverflow.com/a/8260383

        p = YoutubeTool.pattern_url()
        video_id = '5Y6HSHwhVlY'
        urls = [
            f"http://youtu.be/{video_id}",
            f"http://www.youtube.com/embed/{video_id}?rel=0",
            f"http://www.youtube.com/watch?v={video_id}",
            f"http://www.youtube.com/watch?v={video_id}&feature=feedrec_grec_index",
            f"http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/{video_id}",
            f"http://www.youtube.com/v/{video_id}?fs=1&amp;hl=en_US&amp;rel=0",
            f"http://www.youtube.com/watch?v={video_id}#t=0m10s",
            f"http://www.youtube.com/embed/{video_id}?rel=0",
            f"http://www.youtube.com/watch?v={video_id}",
            f"https://studio.youtube.com/video/{video_id}/livestreaming",
            f"http://youtu.be/{video_id}",
        ]

        for url in urls:
            logger.debug(pformat({
                'p':p,
                'url':url,
            }))
            self.assertTrue(p.match(url))
            self.assertEqual(YoutubeTool.url2video_id(url), video_id)

    @pytest.mark.skip(reason="'video_id' keep changing")
    def test_05(self):
        credentials = FoxylibGoogleapi.ServiceAccount.credentials()
        youtube_service = YoutubeapiTool.credentials2service(credentials)
        live_chat_id = YoutubeTool.video_id2live_chat_id(youtube_service, 'ePnWBJnj7C0')

        hyp = live_chat_id
        ref = 'Cg0KC2VQbldCSm5qN0MwKicKGFVDTDI5X1pkaENHV3pjMTZ1NW04S19VURILZVBuV0JKbmo3QzA'
        self.assertEqual(live_chat_id, ref)

    def test_06(self):
        video_id = '5Y6HSHwhVlY'
        strs = [
            f"http://youtu.be/{video_id}",
            f"http://www.youtube.com/embed/{video_id}?rel=0",
            f"http://www.youtube.com/watch?v={video_id}",
            f"http://www.youtube.com/watch?v={video_id}&feature=feedrec_grec_index",
            f"http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/{video_id}",
            f"http://www.youtube.com/v/{video_id}?fs=1&amp;hl=en_US&amp;rel=0",
            f"http://www.youtube.com/watch?v={video_id}#t=0m10s",
            f"http://www.youtube.com/embed/{video_id}?rel=0",
            f"http://www.youtube.com/watch?v={video_id}",
            f"http://youtu.be/{video_id}",
            video_id,
        ]
        for str_in in strs:
            self.assertEqual(YoutubeTool.str2video_id(str_in), video_id)
