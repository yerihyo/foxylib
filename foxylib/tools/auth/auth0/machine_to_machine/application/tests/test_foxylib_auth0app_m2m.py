import logging
from pprint import pprint, pformat
from unittest import TestCase

import pytest
from foxylib.tools.collections.collections_tool import l_singleton2obj
from future.utils import lfilter

from foxylib.tools.auth.auth0.foxylib_auth0_api import FoxylibAuth0API
from foxylib.tools.auth.auth0.machine_to_machine.application.foxylib_auth0app_m2m import \
    FoxylibAuth0appM2M
from foxylib.tools.auth.auth0.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool, Auth0Connection
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibAuth0appM2M(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='test_02 covers this')
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        token = FoxylibAuth0appM2M.token()
        logger.debug(pformat({'token':token}))
        self.assertTrue(token)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        # domain = 'https://dev-h1obv042.us.auth0.com'
        identifier = FoxylibAuth0API.identifer()
        token = FoxylibAuth0appM2M.token()

        # payload = {'q': 'email:yerihyo@gmail.com'}
        # payload = {'q': 'email:test@foxytrixy.com'}
        payload = None
        users = Auth0M2MTool.users(identifier, token, payload=payload)
        self.assertIsNotNone(users)

        pprint({'users':users})

    def test_03(self):
        connection = Auth0Connection.username_password_auth()

        email = 'test@foxytrixy.com'
        payload = {'q': f'email:{email}'}

        identifier = FoxylibAuth0API.identifer()
        token = FoxylibAuth0appM2M.token()
        users = Auth0M2MTool.users(identifier, token, payload=payload)

        if users:
            user = l_singleton2obj(filter(lambda u: u['email'] == email, users))
            response_delete = Auth0M2MTool.delete_user(identifier, token, user['user_id'])
            self.assertTrue(response_delete)

        body = {
            "email": "test@foxytrixy.com",
            "connection": connection,
            "password": 'efijefji3$3',
            "email_verified": False,
        }
        response_create = Auth0M2MTool.create_user(identifier, token, body)
        self.assertIsNotNone(response_create)
