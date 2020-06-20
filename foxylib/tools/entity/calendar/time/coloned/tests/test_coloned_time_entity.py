import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.entity.calendar.time.coloned.coloned_time_entity import ColonedTimeEntity
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestColonedTimeEntity(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = ColonedTimeEntity.data2entity_list({"text_in": "12:20 pm"})
        ref = [{'fulltext': '12:20 pm',
                'span': (0, 8),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'ampm': 'PM', 'hour': 12, 'minute': 20}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = ColonedTimeEntity.data2entity_list({"text_in": "12:20"})
        ref = [{'fulltext': '12:20',
                'span': (0, 5),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'hour': 12, 'minute': 20}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_03(self):
        hyp = ColonedTimeEntity.data2entity_list({"text_in": "15:20"})
        ref = [{'fulltext': '15:20',
                'span': (0, 5),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'hour': 15, 'minute': 20}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_04(self):
        hyp = ColonedTimeEntity.data2entity_list({"text_in": "11:40pm"})
        ref = [{'fulltext': '11:40pm',
                'span': (0, 7),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'ampm': 'PM', 'hour': 11, 'minute': 40}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_05(self):
        hyp = ColonedTimeEntity.data2entity_list({"text_in": "2:30 pm"})
        ref = [{'fulltext': '2:30 pm',
                'span': (0, 7),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'ampm': 'PM', 'hour': 2, 'minute': 30}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)
