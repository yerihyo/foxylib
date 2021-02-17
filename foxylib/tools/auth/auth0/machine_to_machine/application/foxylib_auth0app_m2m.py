import logging
import os
from functools import reduce

import requests

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.auth.auth0.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 4, FILE_DIR)


class FoxylibAuth0appM2M:
    @classmethod
    def domain(cls):
        return FoxylibEnv.key2value("AUTH0_TENANT_URL")

    @classmethod
    def client_id(cls):
        return FoxylibEnv.key2value("AUTH0_M2M_CLIENT_ID")

    @classmethod
    def client_secret(cls):
        return FoxylibEnv.key2value("AUTH0_M2M_CLIENT_SECRET")

    @classmethod
    def audience(cls):
        return f'{cls.domain()}/api/v2/'

    @classmethod
    def token(cls):
        domain = cls.domain()

        payload = {'client_id': cls.client_id(),
                   'client_secret': cls.client_secret(),
                   'audience': cls.audience(),
                   'grant_type': 'client_credentials',
                   }
        token = Auth0M2MTool.payload2token(domain, payload)
        return token

    @classmethod
    def users(cls):
        logger = FoxylibLogger.func_level2logger(cls.users, logging.DEBUG)

        url = f'{cls.domain()}/api/v2/users'
        token = cls.token()
        logger.debug({'token':token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(url, headers=headers,)

        j_response = response.json()

        return j_response


