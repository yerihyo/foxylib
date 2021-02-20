import logging
from pprint import pprint, pformat
from unittest import TestCase

import pytest

from foxylib.tools.auth.auth0.application.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool, Auth0Connection, Auth0User
from foxylib.tools.auth.auth0.application.machine_to_machine.foxylib_auth0app_m2m import \
    FoxylibAuth0appM2M, TicketOption
from foxylib.tools.auth.auth0.auth0_tool import Auth0Tool
from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import FailedRequest


class TestFoxylibAuth0appM2M(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='test_02 covers this')
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        app_info = FoxylibAuth0appM2M.app_info()
        token = app_info.token()
        logger.debug(pformat({'token':token}))
        self.assertTrue(token)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        app_info = FoxylibAuth0appM2M.app_info()

        payload = {'q': 'email:test@foxytrixy.com'}
        users = Auth0M2MTool.users(app_info, payload=payload)
        self.assertIsNotNone(users)

        pprint({'users':users})

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_03, logging.DEBUG)

        connection = Auth0Connection.username_password_auth()

        email = 'test@foxytrixy.com'
        payload = {'q': f'email:{email}'}

        app_info = FoxylibAuth0appM2M.app_info()
        users = Auth0M2MTool.users(app_info, payload=payload)

        if users:
            user = l_singleton2obj(filter(lambda u: u['email'] == email, users))
            deleted_succeeded = Auth0M2MTool.delete_user(app_info, user.user_id)
            self.assertTrue(deleted_succeeded)

        body = {
            "email": email,
            "connection": connection,
            "password": Auth0Tool.generate_password(),
            "email_verified": False,
        }
        user = Auth0M2MTool.create_user(app_info, body)
        self.assertIsNotNone(user)

        with self.assertRaises(FailedRequest) as context:
            Auth0M2MTool.create_user(app_info, body)
        self.assertEqual(context.exception.response.status_code, 409)

        q = Auth0M2MTool.Q.qitems2q([
            Auth0M2MTool.Q.connection2qitem(connection),
            Auth0M2MTool.Q.email2qitem(email),
        ])
        user = Auth0M2MTool.q2user(app_info, q)
        self.assertTrue(user.user_id)

        # callback_url = 'http://localhost:3000/'

        website_name = 'asdfasdfa'
        url_invitation = TicketOption.user_id2url_invitation(
            app_info, user.user_id, website_name)
        logger.debug({'url_invitation': url_invitation})
        self.assertTrue(url_invitation)
        self.assertIn(website_name, url_invitation)
