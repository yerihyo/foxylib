import calendar
import copy
import math
import os
from datetime import datetime, timedelta, date, time

import arrow
import pytz
from dateutil.relativedelta import relativedelta
from future.utils import lmap
from nose.tools import assert_equal, assert_greater

from foxylib.tools.arithmetic.arithmetic_tool import ArithmeticTool
from foxylib.tools.collections.collections_tool import ListTool
from foxylib.tools.collections.iter_tool import IterTool
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
    class Value:
        MILLISEC = "millisec"


class DatetimeTool:
    @classmethod
    def datetime2truncate_seconds(cls, dt):
        return copy.copy(dt).replace(second=0, microsecond=0)


    @classmethod
    def datetime2nearest(cls, dt_from, dt_pivot, td_period, nearest):
        td = dt_pivot - dt_from

        # td_unit = timedelta(days=1)

        def nearest2q(n):
            q = td / td_period

            if n == Nearest.PAST:
                return math.floor(q)

            elif n == Nearest.COMING:
                return math.ceil(q)

            else:
                return round(q)

        qq = nearest2q(nearest)

        # raise Exception({"dt_from": dt_from,
        #                  "dt_pivot": dt_pivot,
        #                  "td":td,
        #                  "td_period": td_period,
        #                  "qq": qq,
        #                  })

        return dt_from + td_period * qq

    @classmethod
    def from_pivot_period2next(cls, dt_from, dt_pivot, td_period):
        # utc_now = datetime.now(pytz.utc)

        q = ArithmeticTool.divide_and_ceil(dt_pivot - dt_from, td_period)
        dt_out = dt_from + q * td_period
        return dt_out



    @classmethod
    def fromisoformat(cls, str_in):
        return arrow.get("2019-08-19T00:44:40.912587+00:00").datetime

    @classmethod
    def truncate(cls, dt_in, unit):
        if unit == DatetimeUnit.Value.MILLISEC:
            microsec = dt_in.microsecond // 1000 * 1000
            return datetime(dt_in.year, dt_in.month, dt_in.day, dt_in.hour, dt_in.minute, dt_in.second, microsec)

        raise NotImplementedError("Unsupported unit: {}".format(unit))


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
    def astimezone(cls, dt, tz):
        return dt.astimezone(tz)

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


class TimedeltaTool:
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
    def timedelta_unit2quotient(cls, td, unit):
        return td // unit

    @classmethod
    def timedelta_unit2remainder(cls, td, unit):
        return td % unit

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

            span_fullweek = SpanTool.span_size2valid(span_fullweek_raw, n)
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
    def time2datetime_nearest(cls, time_from, datetime_pivot, timedelta_unit, nearest):
        dt_from = datetime.combine(datetime_pivot.date(), time_from, tzinfo=time_from.tzinfo)
        return DatetimeTool.datetime2nearest(dt_from, datetime_pivot, timedelta_unit, nearest)


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