import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.entity.calendar.time.hour_ampm.hour_ampm_time_entity import HourAMPMTimeEntity
from foxylib.tools.entity.calendar.time.time_entity import TimeEntity
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestTimeEntity(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = TimeEntity.text2entity_list("4:04pm")
        ref = [{'fulltext': '4:04pm',
  'span': (0, 6),
  'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
  'value': {'ampm': 'PM', 'hour': 4, 'minute': 4}}]

        pprint(hyp)
        self.assertEqual(hyp, ref)
