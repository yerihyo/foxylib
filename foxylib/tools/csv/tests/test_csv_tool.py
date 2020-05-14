import logging
import os
from pprint import pprint
from unittest import TestCase

from foxylib.tools.csv.csv_tool import CSVTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestCSVTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        filepath = os.path.join(FILE_DIR, "test.csv")
        str_ll = CSVTool.filepath2str_ll(filepath)

        hyp = str_ll
        ref = [['a1', 'a2'],
               ['b1', 'b2', 'b3'],
               ['c1', 'c2', 'c3', 'c4'],
               ['d11,d12', 'd2', 'd3']]

        # pprint(hyp)
        self.assertEqual(hyp, ref)