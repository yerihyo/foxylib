import logging
import os
from functools import reduce, lru_cache

import requests
from dacite import from_dict

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.auth.auth0.application.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool, Auth0M2MInfo
from foxylib.tools.auth.auth0.foxylib_auth0_api import FoxylibAuth0API
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 4, FILE_DIR)


class FoxylibAuth0appM2M:
    @classmethod
    def domain(cls):
        return FoxylibEnv.key2value("AUTH0_DOMAIN")

    @classmethod
    def client_id(cls):
        return FoxylibEnv.key2value("AUTH0_M2M_CLIENT_ID")

    @classmethod
    def client_secret(cls):
        return FoxylibEnv.key2value("AUTH0_M2M_CLIENT_SECRET")

    @classmethod
    @lru_cache(maxsize=2)
    def m2m_info(cls) -> Auth0M2MInfo:
        j_info = {
            'api_info':FoxylibAuth0API.api_info(),
            'client_id':cls.client_id(),
            'client_secret':cls.client_secret(),
        }
        m2m_info = from_dict(Auth0M2MInfo, j_info)
        return m2m_info

    @classmethod
    def users(cls):
        logger = FoxylibLogger.func_level2logger(cls.users, logging.DEBUG)

        url = f'{cls.domain()}/api/v2/users'
        token =  cls.m2m_info().token()
        logger.debug({'token':token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(url, headers=headers,)

        j_response = response.json()

        return j_response


