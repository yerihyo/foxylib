import logging
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

import dateutil.parser
import pytz

from foxylib.tools.collections.collections_tool import CollectionTool
from foxylib.tools.datetime.datetime_tool import DatetimeTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.number.decimal_tool import DecimalTool


class TestJsonTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        transducer_tree = {
            'a': Decimal,
            'b': CollectionTool.func2traversing(Decimal),
            'c': {'d': CollectionTool.func2traversing(dateutil.parser.parse)},
        }

        j_in = {"a": '34',
                'b': '54',
                'c': {'d': ['2020-11-18T01:00:00+00:00',
                            '2020-11-18T02:00:00+00:00']},

                }
        h_out = JsonTool.transduce_value(j_in, transducer_tree)

        # pprint(h_out)
        ref = {'a': Decimal('34'),
               'b': Decimal('54'),
               'c': {
                   'd': [datetime(2020, 11, 18, 1, 0, tzinfo=pytz.utc),
                         datetime(2020, 11, 18, 2, 0, tzinfo=pytz.utc)]}}
        self.assertEqual(h_out, ref)

    def test_02(self):
        transducer_tree = {
            'a': lambda a: {'a': Decimal(a)},
            'b': lambda b: {'z': CollectionTool.func2traversing(Decimal)(b)},
            'c': {
                'd': lambda d: {'y': CollectionTool.func2traversing(dateutil.parser.parse)(d)}
            },
        }

        j_in = {"a": '34',
                'b': '54',
                'c': {'d': ['2020-11-18T01:00:00+00:00',
                            '2020-11-18T02:00:00+00:00']},

                }
        h_out = JsonTool.transduce_kv(j_in, transducer_tree)

        # pprint(h_out)
        ref = {'a': Decimal('34'),
               'z': Decimal('54'),
               'c': {
                   'y': [datetime(2020, 11, 18, 1, 0, tzinfo=pytz.utc),
                         datetime(2020, 11, 18, 2, 0, tzinfo=pytz.utc)]}}
        self.assertEqual(h_out, ref)

    def test_03(self):
        transducer_tree = {
            'buffs': {
                'score': lambda x: {'score': DecimalTool.x2decimal(x)},
            }
        }

        j_in = [{'buffs': [{'target': 'bts', 'score': -53.829}]}]
        h_out = JsonTool.transduce_kv(j_in, transducer_tree)

        self.assertEqual(h_out, j_in)
