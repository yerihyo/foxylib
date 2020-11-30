import logging
from datetime import datetime
from decimal import Decimal
from pprint import pprint
from unittest import TestCase

import dateutil.parser
import pytz

from foxylib.tools.collections.collections_tool import CollectionTool
from foxylib.tools.json.json_tool import JsonTool, Json2Native

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestJsonTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        parser_tree = {
            'a': Decimal,
            'b': CollectionTool.func2traversing(Decimal),
            'c': {'d': CollectionTool.func2traversing(dateutil.parser.parse)},
        }

        j_in = {"a": '34',
                'b': '54',
                'c': {'d': ['2020-11-18T01:00:00+00:00',
                            '2020-11-18T02:00:00+00:00']},

                }
        h_out = JsonTool.json2native(j_in, parser_tree)

        # pprint(h_out)
        ref = {'a': Decimal('34'),
               'b': Decimal('54'),
               'c': {
                   'd': [datetime(2020, 11, 18, 1, 0, tzinfo=pytz.utc),
                         datetime(2020, 11, 18, 2, 0, tzinfo=pytz.utc)]}}
        self.assertEqual(h_out, ref)
