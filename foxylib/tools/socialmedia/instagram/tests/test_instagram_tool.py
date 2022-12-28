import logging
import os
import time
from unittest import TestCase

import pytest

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.socialmedia.instagram.instagram_tool import InstagramTool


class TestInstagramTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip('an action. not a real test.')
    def test_01(self):
        sessionid = '1983105748%3AscmoPQLKPTsICR%3A21'

        urls = [
            'https://www.instagram.com/p/CYlZaX4Fdjh/',
            'https://www.instagram.com/p/CYD4CmkFpTX/',
            'https://www.instagram.com/p/CVzeSzsJF8u/',
            'https://www.instagram.com/p/CU4adD4pjzD/',
            'https://www.instagram.com/p/CTI6I8MJuJy/',
            'https://www.instagram.com/p/CSk0OTrpaGp/',
            'https://www.instagram.com/p/CSQEXVXJJUH/',
            'https://www.instagram.com/p/CR-GXkZpaNv/',
            'https://www.instagram.com/p/CRvM95BJpw5/',
            'https://www.instagram.com/p/CPPdtanJnTb/',
            'https://www.instagram.com/p/CNMwECfp-Tg/',
            'https://www.instagram.com/p/CMBeUPipuxK/',
        ]
        out_dirpath = '/Users/moonyoungkang/Downloads/나폴레옹/youtube/flowercake'

        for url in urls:
            filename = url.rstrip('/').split('/')[-1]
            filepath = os.path.join(out_dirpath, f"{filename}.mp4")

            # filepath = f"reel{int(time.time())}.mp4"
            if os.path.exists(filepath):
                continue

            InstagramTool.url2video(url, filepath, sessionid,)

