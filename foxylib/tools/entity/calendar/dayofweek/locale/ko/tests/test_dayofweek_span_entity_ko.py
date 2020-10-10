import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo
from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_span_entity_ko import DayofweekSpanEntityKo
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestDayofweekSpanEntityKo(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        hyp = DayofweekSpanEntityKo.text2entity_list("월-목")
        ref = [{'fulltext': '월-목',
                'span': (0, 3),
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_span_entity.DayofweekSpanEntity',
                'value': ('monday', 'thursday')}]

        # pprint({"hyp": hyp})
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = DayofweekSpanEntityKo.text2entity_list("월 ~ 목요일, 금")
        ref = [{'fulltext': '월 ~ 목요일, 금',
                'span': (9, 10),
                'text': '금',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': ('friday',)},
               {'fulltext': '월 ~ 목요일, 금',
                'span': (0, 7),
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_span_entity.DayofweekSpanEntity',
                'value': ('monday', 'thursday')}]

        # pprint({"hyp": hyp})
        self.assertEqual(hyp, ref)

    def test_03(self):
        hyp = DayofweekSpanEntityKo.text2entity_list("월수금")
        ref = [{'fulltext': '월수금',
                'span': (0, 1),
                'text': '월',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': ('monday',)},
               {'fulltext': '월수금',
                'span': (1, 2),
                'text': '수',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': ('wednesday',)},
               {'fulltext': '월수금',
                'span': (2, 3),
                'text': '금',
                'type': 'foxylib.tools.entity.calendar.dayofweek.dayofweek_entity.DayofweekEntity',
                'value': ('friday',)}]

        # pprint({"hyp": hyp})
        self.assertEqual(hyp, ref)
