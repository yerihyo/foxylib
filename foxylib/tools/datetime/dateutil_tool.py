import os

import dateutil.parser

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
class DateutilTool:
    @classmethod
    def str2datetime(cls, s):
        if not s:
            return None

        return dateutil.parser.parse(s)