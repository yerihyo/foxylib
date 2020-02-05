import logging
import os
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.software.microsoft.msoffice.excel_tool import ExcelTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestExcelTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        filepath = os.path.join(FILE_DIR, "엑셀샘플.xls")
        workbook = ExcelTool.filepath2workbook(filepath)
        str_ll = list(ExcelTool.workbook_sheetname2line_iter(workbook, "함수목록"))

        self.assertTrue(str_ll)
        self.assertTrue(any(any(l) for l in str_ll))

        for str_list in str_ll:
            logger.debug({"str_list": str_list})


