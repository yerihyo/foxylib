import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.entity.calendar.time.hour_ampm.hour_ampm_time_entity import HourAMPMTimeEntity
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestHourAMPMTimeEntity(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = HourAMPMTimeEntity.data2entity_list({"text_in": "12pm"})
        ref = [{'fulltext': '12pm',
                'span': (0, 4),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'ampm': 'PM', 'hour': 12, 'minute': 0}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = HourAMPMTimeEntity.data2entity_list({"text_in": "3 am"})
        ref = [{'fulltext': '3 am',
                'span': (0, 4),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'ampm': 'AM', 'hour': 3, 'minute': 0}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_03(self):
        hyp = HourAMPMTimeEntity.data2entity_list({"text_in": "13 am"})
        ref = []

        # pprint(hyp)
        self.assertEqual(hyp, ref)

