import logging
import re
from datetime import time
from functools import lru_cache, partial

from future.utils import lmap
from nose.tools import assert_less, assert_greater, assert_not_equal, assert_greater_equal, assert_in, assert_equal, \
    assert_less_equal

from foxylib.tools.collections.collections_tool import DictTool, lchain
from foxylib.tools.datetime.datetime_tool import TimeTool
from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.clazz.class_tool import ClassTool
from foxylib.tools.nlp.contextfree.contextfree_tool import ContextfreeTool
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import StringTool


class AMPM:
    class Value:
        AM = "AM"
        PM = "PM"

        @classmethod
        def value_set(cls):
            return {cls.AM, cls.PM}

    @classmethod
    def warmup(cls):
        cls.pattern()

    @classmethod
    def time2ampm(cls, time_in):
        hour = time_in.hour
        return cls.Value.PM if hour >= 12 else cls.Value.AM

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern(cls):
        rstr = RegexTool.rstr_iter2or([cls.Value.AM, cls.Value.PM])
        return re.compile(rstr, re.I)

    # @classmethod
    # def text2match_list(cls, text):
    #     return list(cls.pattern().finditer(text))

    @classmethod
    def norm(cls, str_in):
        return str_in.upper()

    @classmethod
    def match2value(cls, m):
        v = cls.norm(m.group())
        assert_in(v, cls.Value.value_set())
        return v

    @classmethod
    def hour2ampmed(cls, hour_in, ampm):
        if hour_in == 12:
            if ampm == AMPM.Value.AM:
                return 0

            if ampm == AMPM.Value.PM:
                return 12

            return hour_in

        if ampm == AMPM.Value.PM:
            return hour_in + 12

        return hour_in

    @classmethod
    def hour_ampm2normalized(cls, hour_in, ampm):

        """ special treat 0 or 24 since 24 o'clock is not in time() entity """
        if hour_in in {0, 24}:
            if ampm == cls.Value.PM:  # invalid
                return None, ampm

            return 0, cls.Value.AM

        hour = TimeTool.hour2norm(hour_in)
        if hour is None:
            return hour, ampm

        """ special treat 12 """
        if hour == 12:
            if ampm == cls.Value.AM:
                return 0, cls.Value.AM

            return 12, ampm  # ampm can be None or PM

        """ check if hour >= 13 matches AMPM """
        if hour >= 13:  # pm o'clocks
            assert_less_equal(hour, 23)

            if ampm == cls.Value.AM:  # invalid
                return None, ampm

            return hour-12, cls.Value.PM

        if ampm is None:
            return hour, ampm

        if ampm == cls.Value.AM:
            if hour == 12:
                return 0, cls.Value.AM

            assert_greater_equal(hour, 0)

            if hour > 12:
                return None, ampm

            return hour, cls.Value.AM

        if ampm == cls.Value.PM:
            assert_greater(hour, 0)
            assert_less_equal(hour, 12)

            hour_out = hour # if hour >= 12 else hour + 12

            # assert_greater_equal(hour_out, 12)
            # assert_less(hour_out, 23)
            return hour_out, cls.Value.PM

        raise RuntimeError("Invalid ampm: {}".format(ampm))


class TimeEntity:
    @classmethod
    def entity_type(cls):
        return ClassTool.class2fullpath(cls)

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_digit_1or2(cls):
        return re.compile(r"\d{1,2}")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_digit_2(cls):
        return re.compile(r"\d{2}")

    @classmethod
    def warmup(cls):
        AMPM.warmup()

        cls.pattern_digit_1or2()
        cls.pattern_digit_2()

        from foxylib.tools.entity.calendar.time.coloned.coloned_time_entity import ColonedTimeEntity
        ColonedTimeEntity.warmup()

        # from foxylib.tools.entity.calendar.time.hour_ampm.hour_ampm_time_entity import HourAMPMTimeEntity
        # HourAMPMTimeEntity.warmup()

    class Data:
        class Field:
            TEXT_IN = "text_in"
            MATCH_LIST_AMPM = "match_list_ampm"
            MATCH_LIST_DIGIT_1OR2 = "match_list_digit_1or2"
            MATCH_LIST_DIGIT_2 = "match_list_digit_2"

        @classmethod
        def data2text_in(cls, data):
            return data[cls.Field.TEXT_IN]

        @classmethod
        def data2match_list_ampm(cls, data):
            if cls.Field.MATCH_LIST_AMPM not in data:
                data[cls.Field.MATCH_LIST_AMPM] = list(AMPM.pattern().finditer(cls.data2text_in(data)))

            return data[cls.Field.MATCH_LIST_AMPM]

        @classmethod
        def data2match_list_digit_1or2(cls, data):
            if cls.Field.MATCH_LIST_DIGIT_1OR2 not in data:
                text_in = cls.data2text_in(data)
                data[cls.Field.MATCH_LIST_DIGIT_1OR2] = list(TimeEntity.pattern_digit_1or2().finditer(text_in))

            return data[cls.Field.MATCH_LIST_DIGIT_1OR2]

        @classmethod
        def data2match_list_digit_2(cls, data):
            if cls.Field.MATCH_LIST_DIGIT_2 not in data:
                text_in = cls.data2text_in(data)
                data[cls.Field.MATCH_LIST_DIGIT_2] = list(TimeEntity.pattern_digit_2().finditer(text_in))

            return data[cls.Field.MATCH_LIST_DIGIT_2]

    class Value:
        class Field:
            HOUR = "hour"
            MINUTE = "minute"
            SECOND = "second"
            AMPM = "ampm"

        @classmethod
        def value2hour(cls, v):
            return v[cls.Field.HOUR]

        @classmethod
        def value2minute(cls, v):
            return v[cls.Field.MINUTE]

        @classmethod
        def value2second(cls, v):
            return v.get(cls.Field.SECOND)

        @classmethod
        def value2hm(cls, v):
            return cls.value2hour(v), cls.value2minute(v)

        @classmethod
        def value2hms(cls, v):
            return cls.value2hour(v), cls.value2minute(v), cls.value2second(v)

        @classmethod
        def value2ampm(cls, v):
            return v.get(cls.Field.AMPM)

    @classmethod
    def time2value(cls, time_in):
        ampm = AMPM.time2ampm(time_in)
        v = {cls.Value.Field.HOUR: time_in.hour,
             cls.Value.Field.MINUTE: time_in.minute,
             cls.Value.Field.SECOND: time_in.second,
             cls.Value.Field.AMPM: ampm,
             }
        return v

    @classmethod
    def value2datetime_time(cls, v):
        h_raw, m, s = cls.Value.value2hms(v)
        ampm_raw = cls.Value.value2ampm(v)

        h = AMPM.hour2ampmed(h_raw, ampm_raw)

        if s is None:
            return time(hour=h, minute=m)
        else:
            return time(hour=h, minute=m, second=s)

    @classmethod
    def entity_list2ampm_suffixed(cls, data, entity_list_in,):
        logger = FoxylibLogger.func_level2logger(cls.entity_list2ampm_suffixed, logging.DEBUG)

        text_in = cls.Data.data2text_in(data)
        m_list_ampm = cls.Data.data2match_list_ampm(data)

        span_list_in = lmap(FoxylibEntity.entity2span, entity_list_in)
        span_list_ampm = lmap(lambda m: m.span(), m_list_ampm)

        spans_list = [span_list_in, span_list_ampm]
        gap2is_valid = partial(StringTool.str_span2match_blank_or_nullstr, text_in)
        indextuple_list = ContextfreeTool.spans_list2reducible_indextuple_list(spans_list, gap2is_valid)
        h_i2j = dict(indextuple_list)

        def i2entity(i):
            entity = entity_list_in[i]
            assert_equal(FoxylibEntity.entity2type(entity), TimeEntity.entity_type())

            if i not in h_i2j:
                return entity_list_in[i]

            j = h_i2j[i]

            m_ampm = m_list_ampm[j]
            span = (span_list_in[i][0], span_list_ampm[j][1])

            v_entity = FoxylibEntity.entity2value(entity)
            hour, minute, second = TimeEntity.Value.value2hms(v_entity)
            ampm = AMPM.match2value(m_ampm)
            hour_adjusted, ampm_adjusted = AMPM.hour_ampm2normalized(hour, ampm)

            # logger.debug({"hour":hour, "ampm":ampm,
            #               "hour_adjusted":hour_adjusted, "ampm_adjusted":ampm_adjusted})

            value = DictTool.filter(lambda k, v: v,
                                    {TimeEntity.Value.Field.HOUR: hour_adjusted,
                                     TimeEntity.Value.Field.MINUTE: minute,
                                     TimeEntity.Value.Field.SECOND: second,
                                     TimeEntity.Value.Field.AMPM: ampm_adjusted,
                                     })

            entity = {FoxylibEntity.Field.TYPE: FoxylibEntity.entity2type(entity),
                      FoxylibEntity.Field.FULLTEXT: text_in,
                      FoxylibEntity.Field.SPAN: span,
                      FoxylibEntity.Field.VALUE: value,
                      }
            return entity

        entity_list = lmap(i2entity, range(len(entity_list_in)))
        return entity_list

    @classmethod
    def text2entity_list(cls, text_in):
        data = {cls.Data.Field.TEXT_IN: text_in,
                }

        from foxylib.tools.entity.calendar.time.hour_ampm.hour_ampm_time_entity import HourAMPMTimeEntity
        entity_list_hour_ampm = HourAMPMTimeEntity.data2entity_list(data)

        from foxylib.tools.entity.calendar.time.coloned.coloned_time_entity import ColonedTimeEntity
        entity_list_coloned = ColonedTimeEntity.data2entity_list(data)

        entity_list = lchain(entity_list_hour_ampm, entity_list_coloned)
        return entity_list
