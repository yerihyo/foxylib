import logging
from unittest import TestCase

from flask import Response

from foxylib.tools.auth.auth0.foxylib_auth0 import FoxylibAuth0
from foxylib.tools.flask.foxylib_flask import FoxylibFlask
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibAuth0(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        app = FoxylibAuth0.add_auth02app(FoxylibFlask.app())
        c = app.test_client()

        response = c.get(FoxylibAuth0.V.URL_LOGIN)
        self.assertEqual(response.status_code, 302)
        # logger.debug({"response.data": response.data,})
