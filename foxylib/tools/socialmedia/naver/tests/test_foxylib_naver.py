import logging
from unittest import TestCase

import pytest
import requests

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.socialmedia.naver.foxylib_naver import FoxylibNaver
from foxylib.tools.url.url_tool import URLTool


class TestFoxylibNaver(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="one time thing for auth token")
    def test_01(self):
        redirect_url = "http://www.way2gosu.com/api/member/oauth2c"

        client_id = FoxylibNaver.client_id()
        url = URLTool.append_query2url("https://nid.naver.com/oauth2.0/authorize",
                                       {"response_type": "code",
                                        "client_id": client_id,
                                        "redirect_uri": redirect_url}
                                       )
        requests.get(url)  # one-time thing to get auth_token

        # redirected: http://www.way2gosu.com/api/member/oauth2c?code=rd9q1nEVlCQmPhWvk3&state=

    @pytest.mark.skip(reason="can't make it work yet")
    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        token = FoxylibNaver.foxytrixy_auth_token()
        # token = "YOUR_ACCESS_TOKEN"
        # header = "Bearer {}".format(token)
        clubid = "29510017" # torymon
        url = "https://openapi.naver.com/v1/cafe/" + clubid + "/members"
        # nickname = urllib.parse.quote("foxytrixy")
        # data = "nickname=" + nickname
        j_data = {"nickname":"foxytrixy"}

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer {}".format(token),
        }
        response = requests.post(url, json=j_data, headers=headers)

        logger.debug({"response":response,
                      "response.json()":response.json(),
                      })

        # request = urllib.request.Request(url, data=data.encode("utf-8"))
        # request.add_header("Authorization", header)
        # response = urllib.request.urlopen(request)


        self.assertTrue(response.ok)
        # rescode = response.getcode()
        # if (rescode == 200):
        #     response_body = response.read()
        #     print(response_body.decode('utf-8'))
        # else:
        #     print("Error Code:" + rescode)

