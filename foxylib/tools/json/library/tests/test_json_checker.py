import logging
from typing import Optional
from unittest import TestCase

from json_checker import Checker

from foxylib.tools.log.foxylib_logger import FoxylibLogger

"""
references:
https://pypi.org/project/jsonschema/ => no semantic check (e.g. semantically invalid key)
https://pypi.org/project/json-checker/ 
https://pypi.org/project/typing-json/
https://pypi.org/project/typed-tree/

dataclass
"""
class TestJsonschema(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        Checker(int).validate(123)
        Checker(Optional[int]).validate(123)
