import logging
from datetime import datetime
from typing import Any, Optional, Callable
from unittest import TestCase

from foxylib.tools.json.json_typecheck_tool import JsonTypecheckTool, Schema
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestJsonTypecheckTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        j_in = {'a': ['b', 'c', 'd']}
        schema_in = {'a': [str]}
        self.assertTrue(JsonTypecheckTool.xson2is_valid(j_in, schema_in,))
        self.assertFalse(JsonTypecheckTool.xson2is_valid(j_in, {'a': [int]}))
        self.assertFalse(JsonTypecheckTool.xson2is_valid({}, schema_in))

    def test_02(self):
        j_in = {'a': [{'b': 'c'}, {'b': 'd'}, ]}
        schema_in = {'a': [{'b': str}]}
        self.assertTrue(JsonTypecheckTool.xson2is_valid(j_in, schema_in))
        self.assertTrue(JsonTypecheckTool.xson2is_valid(j_in, {'a': [Any]}))
        self.assertFalse(JsonTypecheckTool.xson2is_valid(j_in, {'a': [str]}))
        self.assertFalse(JsonTypecheckTool.xson2is_valid(
            {'a': [{'b': 'c'}, {'c': 'd'}, ]}, schema_in))

    def test_03(self):
        schema = {
                'channel_key': Optional,
                'program_id': Optional,
                'text': str,
                'donation_usd': Optional,
                'ingest_at': datetime,
            }

        json_01 = {
            'text':'hello',
            'ingest_at':datetime.now(),
            'program_id':None,
        }
        JsonTypecheckTool.xson2typechecked(json_01, schema)

    def test_04(self):
        schema = {
            'native2bson': Callable,
            'bson2native': Callable,
        }
        j = {
            'native2bson': lambda x:x,
            'bson2native': lambda x:x,
        }
        policy = JsonTypecheckTool.Policy.FULL

        self.assertTrue(
            JsonTypecheckTool.xson2is_valid(j, schema, policy=policy)
        )

    # def test_05(self):
    #     schema = {
    #         'a': Schema.Optional({
    #             'b':{'c':str}
    #         }),
    #         'd': int,
    #     }
    #
    #     j1 = {'d': 3}
    #     policy = JsonTypecheckTool.Policy.FULL
    #     self.assertTrue(
    #         JsonTypecheckTool.xson2is_valid(j1, schema, policy=policy)
    #     )
    #
    #     j2 = {'a': {'b': {'c': 'aljil'}}, 'd': 3}
    #     policy = JsonTypecheckTool.Policy.FULL
    #     self.assertTrue(
    #         JsonTypecheckTool.xson2is_valid(j2, schema, policy=policy)
    #     )
