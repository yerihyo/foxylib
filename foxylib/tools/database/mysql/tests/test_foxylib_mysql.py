import logging
from unittest import TestCase

from foxylib.tools.database.mysql.foxylib_mysql import SampleTable
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibMysql(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        with SampleTable.values2cursor(['a','b','c','d','e']) as c:
            self.assertTrue(list(c))
