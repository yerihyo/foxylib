# https://www.sitepoint.com/using-python-parse-spreadsheet-data/

import xlrd
from future.utils import lmap


class ExcelTool:
    @classmethod
    def filepath2workbook(cls, filepath, *_, **__):
        return xlrd.open_workbook(filepath, *_, **__)

    @classmethod
    def workbook2sheetname_list(cls, workbook):
        return workbook.sheet_names()

    @classmethod
    def workbook_sheetname2line_iter(cls, workbook, sheetname):
        worksheet = workbook.sheet_by_name(sheetname)

        for row in worksheet.get_rows():
            value_list = lmap(lambda c: c.value, row)
            yield value_list

    @classmethod
    def workbook2line_iter(cls, workbook):
        for sheetname in cls.workbook2sheetname_list(workbook):
            yield from cls.workbook_sheetname2line_iter(workbook, sheetname)

    @classmethod
    def bytes2workbook(cls, bytes):
        return xlrd.open_workbook(file_contents=bytes)

    @classmethod
    def workbook2fulltext(cls, workbook):
        return "\n".join([l
                          for sheetname in cls.workbook2sheetname_list(workbook)
                          for l in cls.workbook_sheetname2line_iter(workbook, sheetname)
                          ])
