import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo
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


    def test_04(self):
        hyp = DayofweekEntityKo.str2entity_list("월,수,금")
        ref = [{'span': (0, 1), 'text': '월', 'value': 'monday'},
               {'span': (2, 3), 'text': '수', 'value': 'wednesday'},
               {'span': (4, 5), 'text': '금', 'value': 'friday'}]

        pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_05(self):
        hyp = DayofweekEntityKo.str2entity_list("화목")
        ref = [{'span': (0, 1), 'text': '화', 'value': 'tuesday'},
               {'span': (1, 2), 'text': '목', 'value': 'thursday'},
               ]

        # pprint(hyp)
        self.assertEqual(hyp, ref)
