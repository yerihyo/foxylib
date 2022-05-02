import logging
from dataclasses import dataclass
from pprint import pprint
from typing import List
from unittest import TestCase

import ffmpeg
import pytest
from pytube import YouTube

from foxylib.tools.google.youtube.pytube.pytube_tool import PytubeTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestPytubeTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip("working. action not test")
    def test_1(self):
        YouTube('https://youtu.be/9bZkp7q19f0').streams.first().download()

        yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

    @pytest.mark.skip("working. action not test")
    def test_2(self):
        # youtube = YouTube('https://youtu.be/9bZkp7q19f0')
        youtube = YouTube('https://www.youtube.com/watch?v=AkWW8v9fp7Y')
        # pprint({'youtube.js':youtube.js})

        # ofolder_path = '/Users/moonyoungkang/Downloads/표전/climatechange/series/5_carbon_neutral_2050_car/video'
        ofolder_path = '/tmp'
        ofile_prefix = f'{ofolder_path}/youtube_download'
        ofile_video = f'{ofile_prefix}.video.mp4'
        ofile_audio = f'{ofile_prefix}.audio.mp4'
        ofile_final = f'{ofile_prefix}.mp4'

        youtube.streams.filter(adaptive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()\
            .download(filename=ofile_video)

        youtube.streams.filter(only_audio=True, file_extension='mp4')\
            .first().download(filename=ofile_audio)

        input_video = ffmpeg.input(ofile_video)
        input_audio = ffmpeg.input(ofile_audio)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(ofile_final).run()

    @pytest.mark.skip("working. action not test")
    def test_3(self):
        # ofolder = '/Users/moonyoungkang/Downloads/표전/climatechange/series/7_stratospheric_aerosol_injection/video'
        # ofolder = '/Users/moonyoungkang/Downloads/표전/etc'
        # ofolder = '/Users/moonyoungkang/Creative Cloud Files/climatechange/series/20220331_해양구름표백/video'

        @dataclass
        class Config:
            dirpath: str
            url: str

        configs: List[Config] = [
            # (None, 'https://www.youtube.com/watch?v=1ZQG59_z83I',),
            # (None, 'https://www.youtube.com/watch?v=B0KeUlvWakg'),
            # (None, 'https://www.youtube.com/watch?v=YoZF16PZYoU'),
            # Config(
            #     dirpath='/Users/moonyoungkang/Downloads/ptah/commentvideo',
            #     url='https://www.youtube.com/watch?v=OKjV2SQfKrw',
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220415_2018_worldcup_korea_germany/source/videos',
            #     url='https://www.youtube.com/watch?v=GWTMWMLgoiI',
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220415_2018_worldcup_korea_germany/source/videos',
            #     url='https://www.youtube.com/watch?v=qSYE1t6SsAA',
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220415_2018_worldcup_korea_germany/source/videos',
            #     url='https://www.youtube.com/watch?v=_T8WZzA0zjc',
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220415_2018_worldcup_korea_germany/source/videos',
            #     url='https://www.youtube.com/watch?v=-4GAC9CTl1g'
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220419_2014_worldcup_brazil_germany/resources/videos',
            #     url='https://www.youtube.com/watch?v=aE4BdIP6bvc'
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220419_2014_worldcup_brazil_germany/resources/videos',
            #     url='https://www.youtube.com/watch?v=a7IMPsyQg6k'
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Downloads',
            #     url='https://www.youtube.com/watch?v=dt_XJp77-mk'
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220420_bts_dynamite/resources/videos',
            #     url='https://www.youtube.com/watch?v=gdZLi9oWNZg',
            # ),
            # Config(
            #     dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220420_premiereleague_liverpool_v_manchesterunited/resources/videos',
            #     url='https://www.youtube.com/watch?v=8hBQqSE5NfY',
            # ),
            # Config(
            #     dirpath='/tmp',
            #     url='https://www.youtube.com/watch?v=8hBQqSE5NfY',
            # ),
            Config(
                dirpath='/Users/moonyoungkang/Creative Cloud Files/series/202204_commentvideo/episodes/20220429_championsleague_machestercity_realmadrid/resources/videos',
                url='https://www.youtube.com/watch?v=3VJPQjyKPMc',
            ),
        ]

        def old():
            # ofolder = '/Users/moonyoungkang/Downloads/표전/climatechange/series/5_carbon_neutral_2050_car/video'
            dirname_urls = [
                # ('20_bluehouse_musicvideo', 'https://www.youtube.com/watch?v=OanYE6Wck3Y',),
                # ('4_volvo', 'https://www.youtube.com/watch?v=dYo4ETQe71c',),
                # ('5_cadillac', 'https://www.youtube.com/watch?v=SI5U8lIzCoo',),
                # ('6_mercedes_benz_beatles', 'https://youtu.be/7fqI5-occgI?t=53',),
                # ('7_avtr', 'https://www.youtube.com/watch?v=ChqM3zqTREQ',),
                # ('8_audi_endgame', 'https://youtu.be/913UNZQD6dY?t=97',),
                # ('9_audi_etron', 'https://www.youtube.com/watch?v=eUKvKz11-bU',),
                # ('10_porsche', 'https://www.youtube.com/watch?v=Krgg6rZ_isY',),
                # ('11_dodge', 'https://www.youtube.com/watch?v=xZNXVuzPio4',),
                # ('12_hyundai', 'https://www.youtube.com/watch?v=sbmk6t5j3cM',),
                # ('13_tesla', 'https://www.youtube.com/watch?v=XB2g7-HgE_g',),
                # ('14_hyundai', 'https://www.youtube.com/watch?v=3n5gJq53waE',),
                # ('15_cadillac', 'https://www.youtube.com/watch?v=SI5U8lIzCoo',),
                # ('16_tesla', 'https://www.youtube.com/watch?v=XB2g7-HgE_g',),
                # ('17_ioniq', 'https://www.youtube.com/watch?v=drq6irgVvMQ',),
                # ('18_seven', 'https://www.youtube.com/watch?v=t04Z9QuTsro',),
                # ('19_skynews', 'https://youtu.be/ZXFXQqv74Lk?t=57',),
                # ('', '',),
                # ('', '',),
                # ('', '',),
                # ('', '',),
            ]

        # for dirname, url in dirname_urls:
        for config in configs:
            # pprint({'url':url})
            PytubeTool.url_dirpath2file(config.url, config.dirpath)
