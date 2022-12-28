import logging
import sys
from contextlib import contextmanager
from functools import wraps
from pprint import pprint

from future.utils import lfilter, lmap
from nose.tools import assert_true

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.function.method_tool import MethodTool


class UnittestTool:
    @classmethod
    @contextmanager
    def assertNoLog(cls, unittest, level):
        # https://stackoverflow.com/questions/56707507/make-unittests-fail-on-logger-warning-calls
        with unittest.assertLogs(level=level) as cm:
            yield
            logging.error(
                "gotcha ! with 1 log, you cannot fail before I check ;p")

        # logging.LogRecord
        # pprint({'level':level,
        #         'cm':cm})

        n = len(cm.output)

        # logging._nameToLevel
        i_list_valid = \
            lfilter(lambda i: cm.records[i].levelno >= level, range(n-1))

        if not i_list_valid: # let's remove this last log
            return

        for i in i_list_valid:
            r = cm.records[i]
            print(r, file=sys.stderr)  # print full failing logs for debug

        raise AssertionError(
            "Log with level >= {level} received".format(level=level),
            lmap(lambda i: cm.output[i], i_list_valid),
        )

