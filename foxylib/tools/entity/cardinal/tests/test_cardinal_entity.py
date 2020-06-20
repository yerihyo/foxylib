import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.entity.cardinal.cardinal_entity import CardinalEntity
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestCardinalEntity(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = CardinalEntity.text2entity_list("46")
        ref = [{'fulltext': '46', 'span': (0, 2), 'text': '46', 'value': 46}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)
