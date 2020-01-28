import logging
from unittest import TestCase

from foxylib.tools.entity.cardinal.cardinal_entity import CardinalEntity
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestCardinalEntity(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)


    def test_01(self):
        hyp = CardinalEntity.str2entity_list("46")
        ref = [{'span': (0, 2), 'text': '46', 'value': 46}]

        self.assertEqual(hyp, ref)
