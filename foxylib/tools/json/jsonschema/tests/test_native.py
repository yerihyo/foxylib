import logging
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from jsonschema import validate, ValidationError, SchemaError, Draft7Validator, \
    validators

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

        # partial validation allowed by default?
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
        with self.assertRaises(SchemaError):
            validate(instance=j_in, schema=schema)

    def test_03(self):

        j_in = {"c": 3, 'd': False}

        schema = {
            'type':'object',
            'properties': {
                'c': {'type':'integer'},
                'd': {'type':'boolean'},
            }
        }

        validate(instance=j_in, schema=schema)

    def test_04(self):

        BaseVal = Draft7Validator
        datetime_checker = BaseVal.TYPE_CHECKER.redefine_many(
            {'asdf':lambda checker, x: isinstance(x, datetime)},
        )

        j_in = {"c": 3, 'd': {'e': datetime.now(), 'f': Decimal(6)}}

        schema = {
            'type': 'object',
            'properties': {
                'c': {'type': 'integer'},
                'd': {
                    'type': 'object',
                    'properties': {
                        'e': {'type': 'asdf', },
                        'f': {'type': 'number', },
                    }
                },
            }
        }

        Validator = validators.extend(BaseVal, type_checker=datetime_checker)
        Validator(schema=schema).validate(instance=j_in)

    def test_05(self):
        j_in = {"c": [3, datetime.now(), lambda x: 'helloworld', {'d': 'e'}], }

        schema = {
            'type': 'object',
            'properties': {
                'c': {'type': 'array'},
            },
            'additionalProperties': False,
            'required': ['c'],
        }

        Draft7Validator(schema=schema).validate(instance=j_in)
