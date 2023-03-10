import logging
from pprint import pprint
from unittest import TestCase

import pytest
import requests

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestKakaomapTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="one time thing for auth token")
    def test_1(self):
        api_key = 'ab6e9b520b52ee37e3a8d4c42feae62c'
        locs = [
            {
                'lat': 37.5889111,
                'lon': 127.005119,
                'query': '나폴레옹과자점',
            },
            {
                'lat': 37.477057,
                'lon': 127.14365,
                'query': '나폴레옹과자점 위례점',
            },
        ]
        headers = {
            'Authorization': f"KakaoAK {api_key}",
        }

        loc = locs[0]
        response = requests.get(
            f"https://dapi.kakao.com/v2/local/search/keyword.json?y={loc['lat']}&x={loc['lon']}&radius=100&query={loc['query']}",
            headers=headers,
        )


        pprint({
            'jdoc_response': response.json()
        })