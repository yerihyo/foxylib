import logging
from pprint import pprint
from unittest import TestCase

import requests

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    """
    https://www.1secmail.com/api/
    """

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        endpoint = "https://www.1secmail.com/api/v1"
        response_getRandomMailbox = requests.get(
            f"{endpoint}/?action=genRandomMailbox&count=1"
        )
        self.assertTrue(response_getRandomMailbox.ok)

        j_body = response_getRandomMailbox.json()
        # pprint({'j_body': j_body, })

        email = j_body[0]
        username, domain = email.split("@")
        response_getMessages = requests.get(
            f"{endpoint}/?action=getMessages&login={username}&domain={domain}"
        )
        self.assertTrue(response_getMessages.ok)

        # messages = response_getMessages.json()


