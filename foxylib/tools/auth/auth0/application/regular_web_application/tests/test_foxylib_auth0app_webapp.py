import logging
from unittest import TestCase

import requests

from foxylib.tools.auth.auth0.foxylib_auth0_api import FoxylibAuth0API
from foxylib.tools.auth.auth0.application.regular_web_application.foxylib_auth0app_webapp import \
    FoxylibAuth0appWebapp
from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import URLTool


class TestFoxylibAuth0appWebapp(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        app, auth0 = FoxylibAuth0appWebapp.app_auth0()

        c = app.test_client()

        response_login = c.get("/auth0/login/", follow_redirects=False)
        # logger.debug({"response.data": response.data,
        #               "response.location": response.location,
        #               })
        self.assertEqual(response_login.status_code, 302)

        url_auth0 = response_login.location
        domain = FoxylibAuth0API.domain()
        self.assertTrue(url_auth0.startswith(f"{domain}/authorize"))

        h_next = URLTool.url2h_query(url_auth0)
        redirect_uri = l_singleton2obj(h_next.get("redirect_uri"))
        self.assertEqual(redirect_uri, "http://localhost:5000/auth0/callback/")


        response_auth0 = requests.get(url_auth0)
        logger.debug({"response_auth0":response_auth0,
                      # "response_auth0.text": response_auth0.text,
                      # "response_auth0.content": response_auth0.content,
                      })

        self.assertEqual(response_auth0.status_code, 200)
        # FileTool.utf82file(response_auth0.text, "/tmp/t.html")

        app_name = FoxylibAuth0appWebapp.name()
        self.assertIn(f"Log in to {app_name}", response_auth0.text)
        self.assertIn(f"Log in to dev-8gnjw0rn to continue to {app_name}", response_auth0.text)


