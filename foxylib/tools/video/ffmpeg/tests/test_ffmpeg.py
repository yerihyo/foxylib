import os
import subprocess
from unittest import TestCase

import ffmpeg
import pytest

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestNative(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='NOT SURE WORKING. ')
    def test_1(self):
        ffmpeg.input(
            '/Users/moonyoungkang/Downloads/표전/climatechange/series/6_carbon_neutral_2050_electricity/video/4_kawasaki/Kawasaki Installation of Liquefied Hydrogen Storage Tank.mp4',
            re=True,

        ).output('rtmp://a.rtmp.youtube.com/live2/ff7y-axck-03re-khyf-4fjb')
        # https://flashphoner.com/how-to-grab-a-video-from-youtube-and-share-it-via-webrtc-in-real-time/

    def adsf(self):
        # logger = FoxylibLogger.func_level2logger(self.test_1, logging.DEBUG)
        url = 'https://www.youtube.com/watch?v=9cQT4urTlXM'
        stream_id = 'stream1'
        key = 'ff7y-axck-03re-khyf-4fjb'
        destination = 'rtmp://a.rtmp.youtube.com/live2'

        _youtube_process = subprocess.Popen(('youtube-dl', '-f', '', '--prefer-ffmpeg', '--no-color', '--no-cache-dir',
                                             '--no-progress', '-o', '-', '-f', '22/18', url, '--reject-title',
                                             stream_id), stdout=subprocess.PIPE)
        _ffmpeg_process = subprocess.Popen(('ffmpeg', '-re', '-i', '-', '-preset', 'ultrafast', '-vcodec', 'copy',
                                            '-acodec', 'copy', '-threads', '1', '-f', 'flv',
                                            destination + "/" + key), stdin=_youtube_process.stdout)


