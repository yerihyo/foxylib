import logging
from unittest import TestCase

from foxylib.tools.auth.auth0.auth0_tool import Auth0Tool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestAuth0Tool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        password = Auth0Tool.generate_password()
        logger.debug({'password': password})
