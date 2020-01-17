import logging
from unittest import TestCase

from foxylib.tools.flask.foxylib_flask import FoxylibFlask
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibFlask(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        app = FoxylibFlask.app()

        with app.test_client() as client:
            response = client.get('/health_liveness', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = client.get('/health_readiness', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

