import logging
from unittest import TestCase

from foxylib.tools.entity.calendar.dayofweek.locale.dayofweek_entity_ko import DayofweekEntityKo
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDayofweekEntityKo(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = DayofweekEntityKo.str2entity_list("월")
        ref = [{'span': (0, 1), 'value': 'monday', 'text': '월'}]
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = DayofweekEntityKo.str2entity_list("월요")
        ref = []
        self.assertEqual(hyp, ref)


    def test_03(self):
        hyp = DayofweekEntityKo.str2entity_list("월요일")
        ref = [{'span': (0, 3), 'value': 'monday', 'text': '월요일'}]
        self.assertEqual(hyp, ref)
