import logging
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from jsonschema import ValidationError
from jsonschema.exceptions import UnknownType

from foxylib.tools.collections.dicttree.dicttree_tool import DicttreeTool
from foxylib.tools.json.jsonschema.jsonschema_tool import JsonschemaTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

"""
references:
https://pypi.org/project/jsonschema/ => no semantic check (e.g. semantically invalid key)
https://pypi.org/project/json-checker/ 
https://pypi.org/project/typing-json/
https://pypi.org/project/typed-tree/

dataclass
"""
class TestJsonschemaTool(TestCase):
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
        validator = JsonschemaTool.schema2validator(schema)

        JsonschemaTool.typechecked(
            validator, {"name": "Eggs", "price": 34.99})
        JsonschemaTool.typechecked(validator, {"name": "Eggs", })

        with self.assertRaises(ValidationError):
            JsonschemaTool.typechecked(
                validator, {"name": "Eggs", "price": 'a'})

        JsonschemaTool.typechecked(
            validator, {"name": "Eggs", "price": 34.99, 'b':'c'})

    def test_02(self):

        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
            "required": ['price','name']
        }
        validator = JsonschemaTool.schema2validator(schema)

        JsonschemaTool.typechecked(
            validator, {"name" : "Eggs", "price" : 34.99})
        with self.assertRaises(ValidationError):
            JsonschemaTool.typechecked(validator, {"name": "Eggs",})

        JsonschemaTool.typechecked(
            validator, {"name": "Eggs", "price": 34.99, 'b':'c'})

    def test_03(self):

        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
            "additionalProperties": False,
        }
        validator = JsonschemaTool.schema2validator(schema)

        JsonschemaTool.typechecked(
            validator, {"name" : "Eggs", "price" : 34.99})
        with self.assertRaises(ValidationError):
            JsonschemaTool.typechecked(
                validator, {"name": "Eggs", "price": 34.99, 'b':'c'},)

    def test_04(self):
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
            "required": ['price', 'name'],
            "additionalProperties": False,
        }
        validator = JsonschemaTool.schema2validator(schema)

        JsonschemaTool.typechecked(
            validator, {"name" : "Eggs", "price" : 34.99})
        with self.assertRaises(ValidationError):
            JsonschemaTool.typechecked(
                validator, {"name": "Eggs",})

        with self.assertRaises(ValidationError):
            JsonschemaTool.typechecked(
                validator, {"name": "Eggs", "price": 34.99, 'b':'c'})

    def test_05(self):
        schema_in = {
            "type": "object",
            "properties": {
                "price": {
                    "type": "object",
                    'properties':{
                        'a': {'type': 'str'}
                    },
                    'additionalProperties':False,
                },
                "name": {"type": "string"},
            },
            "required": ['price', 'name'],
            "additionalProperties": False,
        }

        ref = {
            "type": "object",
            "properties": {
                "price": {
                    "type": "object",
                    'properties': {
                        'a': {'type': 'str'}
                    },
                },
                "name": {"type": "string"},
            },
            "required": ['price', 'name'],
        }

        hyp = DicttreeTool.dicttree2keys_removed(
            schema_in, ["additionalProperties"])

        self.assertEqual(hyp, ref)

    def test_06(self):
        schema_in = {
            "type": "object",
            "properties": {
                "price": {
                    "type": "object",
                    'properties':{
                        'a': {'type': 'str'}
                    },
                    'additionalProperties':False,
                },
                "name": {"type": "string"},
            },
            "additionalProperties": False,
        }

        ref = {
            "type": "object",
            "properties": {
                "price": {
                    "type": "object",
                    'properties': {
                        'a': {'type': 'str'}
                    },
                    "required": ['a'],
                    "additionalProperties": False,
                },
                "name": {"type": "string"},
            },
            "required": ['price', 'name'],
            "additionalProperties": False,
        }

        hyp = JsonschemaTool.schema2required_added(schema_in,)

        self.assertEqual(hyp, ref)

    def test_07(self):
        data_in = {"c": 3, 'd': {'e': datetime.now(), 'f': Decimal(6)}}
        definitions = {'asdf': lambda checker, x: isinstance(x, datetime)}

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
        JsonschemaTool.typechecked(
            JsonschemaTool.schema2validator(schema, definitions=definitions),
            data_in,)

        with self.assertRaises(UnknownType):
            JsonschemaTool.typechecked(
                JsonschemaTool.schema2validator(schema,), data_in)

    def test_08(self):
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": ["number",'string','Decimal']},
            },
        }

        validator = JsonschemaTool.schema2validator(
            schema,
            definitions={"Decimal": lambda c, v: isinstance(v, Decimal)},
        )

        JsonschemaTool.typechecked(validator, {"price": "expensive"})
        JsonschemaTool.typechecked(validator, {"price": 3})

    def test_09(self):
        schema_in = {
            "type": "object",
            "properties": {
                "price": {
                    "type": "object",
                    'properties':{
                        'a': {'type': 'str', 'required':True}
                    },
                    'additionalProperties': False,
                },
                "name": {"type": "string"},
            },
            "required": ['price', 'name'],
        }

        ref = {
            "type": "object",
            "properties": {
                "price": {
                    "type": "object",
                    'properties': {
                        'a': {'type': 'str'}
                    },
                    "additionalProperties": False,
                },
                "name": {"type": "string"},
            },
        }

        hyp = JsonschemaTool.schema2required_removed(schema_in,)
        self.assertEqual(hyp, ref)