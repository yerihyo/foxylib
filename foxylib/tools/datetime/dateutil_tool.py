import calendar
import copy
import logging
import math
import os
from datetime import datetime, timedelta, date, time
from pprint import pformat
from typing import Union, Tuple, Optional, Iterable

import arrow
import dateutil.parser
import pytz
from dateutil.relativedelta import relativedelta
from future.utils import lmap
from nose.tools import assert_equal, assert_greater
from pytimeparse.timeparse import timeparse

from foxylib.tools.arithmetic.arithmetic_tool import ArithmeticTool
from foxylib.tools.collections.collections_tool import ListTool
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import IntegerTool
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.version.version_tool import VersionTool

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
class DateutilTool:
    @classmethod
    def str2datetime(cls, s):
        if not s:
            return None

        return dateutil.parser.parse(s)