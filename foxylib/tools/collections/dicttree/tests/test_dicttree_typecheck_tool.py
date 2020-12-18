import logging
from datetime import datetime
from typing import Optional, Callable, Any
from unittest import TestCase

from foxylib.tools.collections.dicttree.dicttree_tool import DicttreeTool
from foxylib.tools.collections.dicttree.dicttree_typecheck_tool import \
    DicttreeTypecheckTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDicttreeTypecheckTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_04(self):
        j_in = {'a': ['b', 'c', 'd']}
        schema_in = {'a': [str]}
        self.assertTrue(DicttreeTypecheckTool.is_type_satisfied(j_in, schema_in,))
        self.assertFalse(DicttreeTypecheckTool.is_type_satisfied(j_in, {'a': [int]}))
        self.assertFalse(DicttreeTypecheckTool.is_type_satisfied({}, schema_in))

    def test_05(self):
        j_in = {'a': [{'b': 'c'}, {'b': 'd'}, ]}
        schema_in = {'a': [{'b': str}]}

        hyp_01 = DicttreeTypecheckTool.is_type_satisfied(j_in, schema_in,)
        self.assertTrue(hyp_01)

        hyp_02 = DicttreeTypecheckTool.is_type_satisfied(j_in, {'a': [Any]})
        self.assertTrue(hyp_02)

        hyp_03 = DicttreeTypecheckTool.is_type_satisfied(j_in, {'a': [str]},)
        self.assertFalse(hyp_03)

        data_04 = {'a': [{'b': 'c'}, {'c': 'd'}, ]}
        hyp_04 = DicttreeTypecheckTool.is_type_satisfied(data_04, schema_in)
        self.assertFalse(hyp_04)

    def test_06(self):
        schema = {
            'text': str,
            'ingest_at': datetime,

            'channel_key': Optional,
            'program_id': Optional,
            'donation_usd': Optional,
        }

        json_01 = {
            'text': 'hello',
            'ingest_at': datetime.now(),
            'program_id': None,
        }

        self.assertEqual(
            set(DicttreeTool.schema2keys_required(schema)),
            {'text', 'ingest_at'}
        )

        DicttreeTypecheckTool.tree2typechecked(json_01, schema)

    def test_07(self):
        schema = {
            'native2bson': Callable,
            'bson2native': Callable,
        }
        j = {
            'native2bson': lambda x:x,
            'bson2native': lambda x:x,
        }

        self.assertTrue(
            DicttreeTypecheckTool.is_type_satisfied(j, schema)
        )
