import logging
from pprint import pprint, pformat
from unittest import TestCase

import pytest
from foxylib.tools.auth.auth0.auth0_tool import Auth0Tool

from foxylib.tools.collections.collections_tool import l_singleton2obj
from future.utils import lfilter

from foxylib.tools.auth.auth0.foxylib_auth0_api import FoxylibAuth0API
from foxylib.tools.auth.auth0.application.machine_to_machine.foxylib_auth0app_m2m import \
    FoxylibAuth0appM2M
from foxylib.tools.auth.auth0.application.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool, Auth0Connection, Auth0User
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibAuth0appM2M(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='test_02 covers this')
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        m2m_info = FoxylibAuth0appM2M.m2m_info()
        token = m2m_info.token()
        logger.debug(pformat({'token':token}))
        self.assertTrue(token)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        m2m_info = FoxylibAuth0appM2M.m2m_info()

        payload = {'q': 'email:test@foxytrixy.com'}
        users = Auth0M2MTool.users(m2m_info, payload=payload)
        self.assertIsNotNone(users)

        pprint({'users':users})

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_03, logging.DEBUG)

        connection = Auth0Connection.username_password_auth()

        email = 'test@foxytrixy.com'
        payload = {'q': f'email:{email}'}

        m2m_info = FoxylibAuth0appM2M.m2m_info()
        users = Auth0M2MTool.users(m2m_info, payload=payload)

        if users:
            user = l_singleton2obj(filter(lambda u: u['email'] == email, users))
            response_delete = Auth0M2MTool.delete_user(m2m_info, user['user_id'])
            self.assertTrue(response_delete)

        body = {
            "email": "test@foxytrixy.com",
            "connection": connection,
            "password": Auth0Tool.generate_password(),
            "email_verified": False,
        }
        response_create = Auth0M2MTool.create_user(m2m_info, body)
        self.assertIsNotNone(response_create)

        user = Auth0M2MTool.email_connection2user(m2m_info, email, connection)
        user_id = Auth0User.user2user_id(user)
        self.assertTrue(user_id)

        callback_url = 'http://localhost:3000/'
        ticket = Auth0M2MTool.create_password_change_ticket(
            m2m_info, user_id,)
        logger.debug({'ticket':ticket})

        self.assertTrue(ticket)

