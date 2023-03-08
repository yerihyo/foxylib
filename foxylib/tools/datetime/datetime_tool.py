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


class Nearest:
    PAST = "past"
    EITHER = "either"
    COMING = "coming"


class DatetimeUnit:
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"
    MILLISECOND = "millisecond"
    MICROSECOND = "microsecond"

    @classmethod
    def unit2timedelta(cls, unit:str) -> timedelta:
        if unit == cls.DAY:
            return timedelta(days=1)

        if unit == cls.HOUR:
            return timedelta(hours=1)

        if unit == cls.MINUTE:
            return timedelta(minutes=1)

        if unit == cls.SECOND:
            return timedelta(seconds=1)

        if unit == cls.MILLISECOND:
            return timedelta(microseconds=1000)

        if unit == cls.MICROSECOND:
            return timedelta(microseconds=1)

        raise NotImplementedError("Not implemented unit: {}".format(unit))


class DatetimeTool:
    @classmethod
    def milli_added(cls, dt):
        return dt + timedelta(milliseconds=1)

    @classmethod
    def date2midnight(cls, d:date):
        return datetime.combine(d, datetime.min.time())

    @classmethod
    def dtspan2midnights(cls, dtspan:Tuple[datetime,datetime]) -> Iterable[datetime]:
        logger = FoxylibLogger.func_level2logger(cls.dtspan2midnights, logging.DEBUG)

        for i, dt in enumerate(dtspan):
            if cls.datetime2midnight(dt) != dt:
                logger.debug(pformat({
                    'dt': dt,
                    'cls.datetime2midnight(dt)': cls.datetime2midnight(dt),
                }))
                raise RuntimeError(dt)

        yield from SpanTool.range(dtspan[0], dtspan[1], timedelta(days=1))


    @classmethod
    def x2datetime(cls, x) -> Optional[datetime]:
        # if x is None:
        #     return None

        if isinstance(x, datetime):
            return x

        return dateutil.parser.parse(x)

    @classmethod
    # @lru_cache(maxsize=1)
    def rstr_iso8601(cls):
        return r'(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?'

    @classmethod
    def str_hm2minutes(cls, s:str) -> int:
        logger = FoxylibLogger.func_level2logger(cls.str_hm2minutes, logging.DEBUG)
        # logger.debug({'s':s,})
        # logger.debug({"s.split(':')": s.split(':')})
        # logger.debug({"lmap(int, reversed(s.split(':')))": lmap(int, reversed(s.split(':')))})
        return sum([v * pow(60, i) for i, v in enumerate(lmap(int, reversed(s.split(':'))))])

    # @classmethod
    # def str2match(cls, s:str):
    #     p = cls.pattern_iso8601()
    #     return RegexTool.pattern_str2match_full(p, s)

    @classmethod
    def dt2is_aware(cls, dt):
        # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
        if dt.tzinfo is None:
            return False

        if dt.tzinfo.utcoffset(dt) is None:
            return False

        return True

    @classmethod
    def dt2is_naive(cls, dt):
        return not cls.dt2is_aware(dt)

    @classmethod
    def round(cls, dt: datetime, unit: str, nearest: str) -> datetime:
        dt_from = cls.truncate(dt, unit)
        return cls.datetime2nearest(dt, dt_from, DatetimeUnit.unit2timedelta(unit), nearest)

    @classmethod
    def floor(cls, dt:datetime, unit:str,) -> datetime:
        return cls.round(dt, unit, Nearest.PAST)

    @classmethod
    def ceil(cls, dt, unit, ):
        return cls.round(dt, unit, Nearest.COMING)

    @classmethod
    def datetime2nearest(
            cls,
            dt_pivot: datetime,
            dt_from: datetime,
            td_period: timedelta,
            nearest: str,
    ) -> datetime:
        td = dt_pivot - dt_from

        # td_unit = timedelta(days=1)

        def nearest2q(n: str) -> float:
            q = td / td_period

            if n == Nearest.PAST:
                return math.floor(q)

            elif n == Nearest.COMING:
                return math.ceil(q)

            else:
                return round(q)

        qq = nearest2q(nearest)
        return dt_from + td_period * qq

    @classmethod
    def floor_milli(cls, dt:datetime, ) -> datetime:
        return cls.floor(dt, DatetimeUnit.MILLISECOND)

    @classmethod
    def datetime2midnight(cls, dt):
        return cls.datetime2time_truncated(dt)

    @classmethod
    def datetime2time_truncated(cls, dt):
        return cls.truncate(dt, DatetimeUnit.HOUR)

    @classmethod
    def truncate(cls, dt: datetime, unit: str) -> datetime:
        if unit == DatetimeUnit.HOUR:
            return dt.replace(hour=0, minute=0, second=0, microsecond=0,)

        if unit == DatetimeUnit.SECOND:
            return dt.replace(second=0, microsecond=0,)

        if unit == DatetimeUnit.MILLISECOND:
            return dt.replace(microsecond=0)

        if unit == DatetimeUnit.MICROSECOND:
            return dt.replace(microsecond=0)

        raise NotImplementedError("Not implemented unit: {}".format(unit))


    @classmethod
    def from_pivot_period2next(cls, dt_from, dt_pivot, td_period):
        # utc_now = datetime.now(pytz.utc)

        q = ArithmeticTool.divide_and_ceil(dt_pivot - dt_from, td_period)
        dt_out = dt_from + q * td_period
        return dt_out

    @classmethod
    def datetime2isoformat(cls, dt: Optional[datetime]):
        if not dt:
            return dt
        return dt.isoformat()

    @classmethod
    def fromisoformat(cls, str_in):
        return arrow.get("2019-08-19T00:44:40.912587+00:00").datetime




    @classmethod
    def iso8601(cls):
        return "%Y-%m-%dT%H:%M:%S"

    @classmethod
    def tz2now(cls, tz):
        return cls.astimezone(datetime.now(pytz.utc), tz)

    @classmethod
    def now_utc(cls):
        return cls.tz2now(pytz.utc)

    @classmethod
    def utc_now_milli(cls) -> datetime:
        return cls.floor_milli(datetime.now(pytz.utc))



    @classmethod
    def astimezone(cls, dt, tz):
        return dt.astimezone(tz)

    @classmethod
    def as_utc(cls, dt):
        return cls.astimezone(dt, pytz.utc)

    @classmethod
    def span2iter(cls, date_span):
        d_start,d_end = date_span
        days = int((d_end - d_start).days)
        for n in range(days):
            yield d_start + timedelta(n)


    @classmethod
    def datetime_pair2days_difference(cls, dt_pair):
        dt_from, dt_to = dt_pair
        assert_equal(dt_from.tzinfo, dt_to.tzinfo)

        date_from = dt_from.date()
        date_to = dt_to.date()

        return (date_to-date_from).days

    # @classmethod
    # def datetime2days_from_now(cls, datetime_in):
    #
    #     dt_from, dt_to = dt_pair
    #     assert_equal(dt_from.tzinfo, dt_to.tzinfo)
    #
    #     date_from = dt_from.date()
    #     date_to = dt_to.date()
    #
    #     return (date_to - date_from).days


    @classmethod
    def datetime_span2years(cls, dt_span):
        """ https://stackoverflow.com/a/765990 """
        dt_start, dt_end = dt_span
        td = dt_end - dt_start
        num_years = int(td.days // 365.2425)
        if dt_start > dt_end - relativedelta(num_years):
            return num_years - 1
        else:
            return num_years

    @classmethod
    def contains(cls, dt_span, dt_pivot):
        return SpanTool.is_in(dt_pivot, dt_span)
        # dt_start, dt_end = dt_span
        # return dt_start <= dt_pivot < dt_end


class TimedeltaTool:
    @classmethod
    def milli(cls):
        return timedelta(milliseconds=1)

    @classmethod
    def td_pair2dt_span(cls, td_pair: Tuple[timedelta, timedelta], dt_offset: datetime) -> Tuple[datetime,datetime]:
        return dt_offset + td_pair[0], dt_offset + td_pair[1]

    @classmethod
    def sum(cls, tds):
        return sum(tds, timedelta(0))

    @classmethod
    def unit_day(cls):
        return timedelta(days=1)

    @classmethod
    def unit_hour(cls):
        return timedelta(seconds=60*60)

    @classmethod
    def unit_minute(cls):
        return timedelta(seconds=60)

    @classmethod
    def unit_second(cls):
        return timedelta(seconds=1)

    @classmethod
    def td_milli(cls):
        return timedelta(microseconds=1)

    @classmethod
    def timedelta_unit2quotient(cls, td, unit):
        return td // unit

    @classmethod
    def timedelta_unit2remainder(cls, td, unit):
        return td % unit

    @classmethod
    def td2secs(cls, td) -> float:
        # if f_round is None:
        #     f_round = round
        secs_float = td / timedelta(seconds=1)
        return secs_float
        # if f_round is None:
        #     return secs_float
        #
        # secs_int = int(f_round(secs_float))
        # return secs_int

    @classmethod
    def dt_span2micros(cls, dt_span):
        return cls.td2micros(SpanTool.span2len(dt_span))

    @classmethod
    def td2micros(cls, td):
        return round(td.total_seconds() * 10**6)

    @classmethod
    def td2millis(cls, td) -> int:
        return round(td.total_seconds() * 10 ** 3)

    # @classmethod
    # def timedelta_unit2round(cls, td, unit):
    #     q = cls.timedelta_unit2quotient(td, unit)
    #     r = cls.timedelta_unit2remainder(td, unit)
    #     return q + (1 if r > 0 else 0)

    @classmethod
    def timedelta_unit_pair2quotient(cls, td, unit, unit_upper):
        assert_greater(unit_upper, unit)
        return cls.timedelta_unit2quotient(td % unit_upper, unit)

    @classmethod
    def timedelta_units2quotients(cls, td, units):
        n = len(units)
        for i in range(n-1):
            assert_greater(units[i], units[i+1])

        def index2quotient(index):
            if index==0:
                return cls.timedelta_unit2quotient(td, units[index])
            else:
                return cls.timedelta_unit_pair2quotient(td, units[index], units[index-1])

        return lmap(index2quotient, range(n))

    @classmethod
    def rune2secs(cls, s: Union[str, int]) -> Union[int, float]:  # e.g. 30s
        if isinstance(s, int):
            return s

        return timeparse(s)

    @classmethod
    def rune2timedelta(cls, s: str) -> timedelta:  # e.g. 30s
        secs = cls.rune2secs(s)
        return timedelta(seconds=secs)

    @classmethod
    def is_negative(cls, td):
        return td < timedelta(0)

    @classmethod
    def secs2rune(cls, secs: Union[int, float]):
        return cls.timedelta2rune(timedelta(seconds=secs))

    @classmethod
    def timedelta2rune(cls, td: timedelta):
        logger = FoxylibLogger.func_level2logger(
            cls.timedelta2rune, logging.DEBUG)

        if cls.is_negative(td):
            td_abs = cls.timedelta2rune(-td)
            return f'- {td_abs}'

        l = []
        if td.days:
            l.append(f"{td.days}d")

        if td.seconds:
            # logger.debug({'td.seconds':td.seconds})

            hrs = td.seconds // 3600
            if hrs:
                l.append(f"{hrs}h")

            mins = td.seconds % 3600 // 60
            if mins:
                l.append(f"{mins}m")

            secs = td.seconds % 60
            if secs:
                l.append(f"{secs}s")

        return " ".join(l)



class DayOfWeek:
    MONDAY = 0
    SUNDAY = 6

    @classmethod
    def add_n(cls, dow, n):
        return (dow + n) % 7

    @classmethod
    def sub_n(cls, dow, n):
        return ((dow - n % 7) + 7) % 7 # just to be safe

    @classmethod
    def incr(cls, dow):
        return cls.add_n(dow, 1)

    @classmethod
    def decr(cls, dow):
        return cls.sub_n(dow, 1)

    @classmethod
    def date2is_dow(cls, d, dow):
        return d.weekday() == dow

    @classmethod
    def date2is_monday(cls, d):
        return cls.date2is_dow(d, cls.MONDAY)

    @classmethod
    def date2is_sunday(cls, d):
        return cls.date2is_dow(d,cls.SUNDAY)


class DateTool:
    @classmethod
    @IterTool.f_iter2f_list
    def date_list2span_list_weekly(cls, date_list, dow_start):
        n = len(date_list)

        start = 0
        for i, d in enumerate(date_list):
            if i == 0:
                continue

            if DayOfWeek.date2is_dow(d, dow_start):
                yield (start, i)
                start = i

        if n:
            yield (start, n)



    @classmethod
    def date_list2span_list_yearly(cls, date_list):
        def is_year_changed(date_list, i):
            return date_list[i - 1].year != date_list[i].year if i>0 else False

        span_list = ListTool.list_detector2span_list(date_list, is_year_changed)
        return span_list

    @classmethod
    @VersionTool.incomplete
    def date_list2chunks_yearly_fullweeks(cls, date_list):
        n = len(date_list)

        def is_year_changed(date_list, i):
            if i==0:
                return False

            return date_list[i-1].year != date_list[i].year



        i_start = 0
        for i, d in enumerate(date_list):
            if not is_year_changed(date_list, i):
                continue

            span_fullweek_raw = cls.date_list_span_weekday2span_fullweek(date_list, (i_start,i), DayOfWeek.SUNDAY)
            i_start = i # update to next

            span_fullweek = SpanTool.cup(span_fullweek_raw, (0,n))
            yield span_fullweek

    @classmethod
    @VersionTool.incomplete
    def date_list_span_weekday2span_fullweek(cls, date_list, span, weekday):
        s0, e0 = span
        count_sunday_future = cls.date_weekday2count(date_list[e0 - 1], weekday)
        count_sunday_past = cls.weekday_date2count(weekday, date_list[s0])
        e1 = (e0 - 1) + count_sunday_future + 1
        s1 = s0 - count_sunday_past
        return (s1, e1)

    @classmethod
    def date2is_end_of_month(cls, d):
        return d.day == calendar.monthrange(d.year, d.month)[1]

    @classmethod
    def date_weekday2count(cls, d, target_weekday):
        return (target_weekday + 7 - d.weekday()) % 7

    @classmethod
    def weekday_date2count(cls, target_weekday, d):
        return (d.weekday() + 7 - target_weekday) % 7


    @classmethod
    def date2is_jan_1st(cls, d):
        return d.month==1 and d.day==1

    @classmethod
    def date2is_dec_31st(cls, d):
        return d.month == 12 and d.day == 31

    @classmethod
    def date_pair2matches_week_boundary(cls, date_pair):
        if not DayOfWeek.date2is_monday(date_pair[0]):
            return False

        if not DayOfWeek.date2is_sunday(date_pair[1]):
            return False

        return True

    @classmethod
    def date_pair2matches_year_boundary(cls, date_pair):
        if not DateTool.date2is_jan_1st(date_pair[0]):
            return False

        if not DateTool.date2is_dec_31st(date_pair[1]):
            return False

        return True

    @classmethod
    def date_locale2str(cls, d, locale):
        from foxylib.tools.locale.locale_tool import LocaleTool
        if LocaleTool.locale2lang(locale) == "ko":
            l = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]
            return l[d.weekday()]

        l = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        return l[d.weekday()]

    @classmethod
    def date2day8(cls, d: Union[date, datetime]) -> int:
        return int(d.strftime('%Y%m%d'))

class TimeTool:
    @classmethod
    def hour2is_valid(cls, h):
        return 0 <= h <= 23

    @classmethod
    def hour2norm(cls, h):
        if not cls.hour2is_valid(h):
            return None

        return 0 if h == 24 else h

    @classmethod
    def minute2is_valid(cls, m):
        return 0 <= m <= 59

    @classmethod
    def minute2norm(cls, m):
        return m if cls.minute2is_valid(m) else None

    @classmethod
    def second2is_valid(cls, s):
        return 0 <= s <= 59

    @classmethod
    def second2norm(cls, s):
        return s if cls.second2is_valid(s) else None

    @classmethod
    def str_hour2time(cls, str_hour):
        if not IntegerTool.number2is_int(str_hour):
            return None

        try:
            return time(int(str_hour))
        except ValueError:
            return None

    @classmethod
    def time_timedelta2adjusted(cls, t, td):
        dt_old = datetime.combine(date.today(), t)
        dt_new = dt_old + td
        return dt_new.time()

    @classmethod
    def time2datetime_nearest(cls, datetime_pivot, time_from, timedelta_unit, nearest):
        dt_from = datetime.combine(datetime_pivot.date(), time_from, tzinfo=time_from.tzinfo)
        return DatetimeTool.datetime2nearest(datetime_pivot, dt_from, timedelta_unit, nearest)


# class TimedeltaTool:
#     class Value:
#         YEAR = "year"
#         MONTH = "month"
#         WEEK = "week"
#         DAY = "day"
#         HOUR = "hour"
#         MINUTE = "minute"
#         SECOND = "second"


# class TimedeltaTool:
#     @classmethod
#     def unit_list(cls):
#         return [timedelta(days=1),
#                 timedelta(hours=1),
#                 timedelta(minutes=1),
#                 timedelta(seconds=1),
#                 ]
#
# class RelativedeltaTool:
#     @classmethod
#     def unit_list(cls):
#         return [relativedelta(years=1),
#                 relativedelta(months=1),
#                 relativedelta(weeks=1),
#                 relativedelta(days=1),
#                 relativedelta(hours=1),
#                 relativedelta(minutes=1),
#                 relativedelta(seconds=1),
#                 ]



tz2now = DatetimeTool.tz2now
now_utc = DatetimeTool.now_utc