import logging
from datetime import datetime
from decimal import Decimal
from pprint import pprint
from unittest import TestCase

import pytz
from toolz import update_in

from foxylib.tools.collections.collections_tool import ListTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestToolz(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        jdoc_in = {'extra': {'choices': [{'aliases': [{'labels': ['name'],
                                                          'text': '방탄소년단'}],
                                             'key': 'bts'},
                                            {'aliases': [{'labels': ['name'],
                                                          'text': '빅뱅'}],
                                             'key': 'bang'},
                                            {'aliases': [{'labels': ['name'],
                                                          'text': '엑소'}],
                                             'key': 'exo'},
                                            {'aliases': [{'labels': ['name'],
                                                          'text': 'HOT'}],
                                             'key': 'hot'}]},
                      'key': 'qRwhmuOXd6xzm55QEIXou',
                      'legitimacy': 'test',
                      'program_type': 'pollbattle/tourney',
                      'started_at': datetime(2019, 1, 1, 0, 0, tzinfo=pytz.utc)}

        v = {'index': 0,
             'key': 'bang vs bts',
             'roundsize': 4,
             'stats': [{'choice_key': 'bts', 'score': Decimal('0')},
                       {'choice_key': 'bang', 'score': Decimal('0')}],
             'title': 'round of 4'}


        hyp = update_in(jdoc_in, ['extra','matches'], lambda l: ListTool.splice(l or [], (0,1), [v]))
        ref = {'extra': {'choices': [{'aliases': [{'labels': ['name'],
                                                          'text': '방탄소년단'}],
                                             'key': 'bts'},
                                            {'aliases': [{'labels': ['name'],
                                                          'text': '빅뱅'}],
                                             'key': 'bang'},
                                            {'aliases': [{'labels': ['name'],
                                                          'text': '엑소'}],
                                             'key': 'exo'},
                                            {'aliases': [{'labels': ['name'],
                                                          'text': 'HOT'}],
                                             'key': 'hot'}],
                         'matches': [{'index': 0,
                                      'key': 'bang vs bts',
                                      'roundsize': 4,
                                      'stats': [{'choice_key': 'bts', 'score': Decimal('0')},
                                                {'choice_key': 'bang', 'score': Decimal('0')}],
                                      'title': 'round of 4'}]
                         },
                      'key': 'qRwhmuOXd6xzm55QEIXou',
                      'legitimacy': 'test',
                      'program_type': 'pollbattle/tourney',
                      'started_at': datetime(2019, 1, 1, 0, 0, tzinfo=pytz.utc),

               }

        pprint({'hyp':hyp, 'ref':ref})
        self.assertEqual(hyp, ref)

