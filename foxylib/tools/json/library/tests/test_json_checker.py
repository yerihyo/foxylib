import logging
from typing import Optional
from unittest import TestCase

import pytest

from foxylib.tools.log.foxylib_logger import FoxylibLogger

"""
references:
https://pypi.org/project/jsonschema/ => no semantic check (e.g. semantically invalid key)
https://pypi.org/project/json-checker/ 
https://pypi.org/project/typing-json/
https://pypi.org/project/typed-tree/

dataclass
"""
class TestJsonChecker(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='json_checker not installed by default')
    def test_01(self):
        from json_checker import Checker

        Checker(int).validate(123)

        # not working
        with self.assertRaises(Exception):
            Checker(Optional[int]).validate(123)
