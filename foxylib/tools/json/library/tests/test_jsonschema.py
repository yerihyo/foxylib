import logging
from datetime import datetime
from typing import Any, Optional, Callable, List
from unittest import TestCase

from jsonschema import validate, Draft3Validator, ValidationError

from foxylib.tools.json.json_typecheck_tool import JsonTypecheckTool, Schema
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
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
        }

        # v = Draft3Validator(schema)
        # v.validate(j_in)
        # schema = {'a': List[int]}
        validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

        with self.assertRaises(ValidationError):
            validate(instance={"name" : 123, "price" : 34.99},
                     schema=schema)

        with self.assertRaises(ValidationError):
            validate(instance={"price" : 34.99},schema=schema)

    def test_02(self):
        j_in = {"name": "Eggs", "price": 34.99}
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string2"},
            },
        }

        # v = Draft3Validator(schema)
        # v.validate(j_in)
        # schema = {'a': List[int]}
        self.assertFalse(validate(instance=j_in, schema=schema))
