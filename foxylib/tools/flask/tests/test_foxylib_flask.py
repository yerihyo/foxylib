from unittest import TestCase

from foxylib.tools.flask.foxylib_flask import FoxylibFlask


class TestFoxylibFlask(TestCase):


    def test_01(self):
        app = FoxylibFlask.app()

        with app.test_client() as client:
            response = client.get('/health_liveness', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = client.get('/health_readiness', follow_redirects=True)
            self.assertEqual(response.status_code, 200)