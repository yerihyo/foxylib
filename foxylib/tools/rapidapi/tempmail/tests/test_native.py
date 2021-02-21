import logging
from unittest import TestCase

import pytest
import requests

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="not working without subscription")
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/%5Cxb4%22F%5Cxca%5Cxd0%5Cxb6v%5Cx0b%5Cx88%5Cx96%5Cxc1U%5Cx91%5Cxf1%5Cx97%5Cxe4/"

        headers = {
            'x-rapidapi-key': "764d88b78dmsh7114fe9c76fbae9p15ae98jsnaa95e9be64d0",
            'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)
