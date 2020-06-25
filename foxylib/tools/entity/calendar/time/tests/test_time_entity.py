import logging
from pprint import pprint
from unittest import TestCase

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

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_02(self):
        hyp = TimeEntity.text2entity_list("9:00am")
        ref = [{'fulltext': '9:00am',
                'span': (0, 6),
                'type': 'foxylib.tools.entity.calendar.time.time_entity.TimeEntity',
                'value': {'ampm': 'AM', 'hour': 9, 'minute': 0}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)
