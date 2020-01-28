import logging
from unittest import TestCase

from foxylib.tools.entity.calendar.timespan.locale.ko.timespan_entity_ko import TimespanEntityKo
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestTimespanEntityKo(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        str_in = "월수금 오후 3-6시"

    def test_02(self):
        str_in = "월-금 10-4"

    def test_03(self):
        str_in = "주말 10시-11시"

    def test_04(self):
        str_in = "화 10 am - 11 pm"

    def test_05(self):
        str_in = "화,목 "
