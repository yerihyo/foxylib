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
        hyp = DayofweekEntityKo.text2entity_list("월")
        ref = [{'fulltext': '월',
                'span': (0, 1),
                'text': '월',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'monday'}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = DayofweekEntityKo.text2entity_list("월요")
        ref = []

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_03(self):
        hyp = DayofweekEntityKo.text2entity_list("월요일")
        ref = [{'fulltext': '월요일',
                'span': (0, 3),
                'text': '월요일',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'monday'}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_04(self):
        hyp = DayofweekEntityKo.text2entity_list("월,수,금")
        ref = [{'fulltext': '월,수,금',
                'span': (0, 1),
                'text': '월',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'monday'},
               {'fulltext': '월,수,금',
                'span': (2, 3),
                'text': '수',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'wednesday'},
               {'fulltext': '월,수,금',
                'span': (4, 5),
                'text': '금',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'friday'}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_05(self):
        hyp = DayofweekEntityKo.text2entity_list("화목")
        ref = [{'fulltext': '화목',
                'span': (0, 1),
                'text': '화',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'tuesday'},
               {'fulltext': '화목',
                'span': (1, 2),
                'text': '목',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': 'thursday'}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)
