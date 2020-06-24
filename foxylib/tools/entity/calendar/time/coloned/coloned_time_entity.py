import logging
import os
import re
import sys
from datetime import time
from functools import lru_cache, partial

from foxylib.tools.collections.collections_tool import lchain
from future.utils import lmap, lfilter

from foxylib.tools.datetime.datetime_tool import TimeTool
from foxylib.tools.entity.calendar.time.time_entity import TimeEntity, AMPM
from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.nlp.contextfree.contextfree_tool import ContextfreeTool
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.span.span_tool import SpanTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class ColonedTimeEntity:
    @classmethod
    def warmup(cls):
        cls.pattern_colon()

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_colon(cls):
        return re.compile(r"\s*:\s*")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_hour(cls):
        left_bounds = RegexTool.left_wordbounds()
        right_bounds = lchain(RegexTool.right_wordbounds(),
                              [r":"],
                              )
        rstr = RegexTool.rstr2bounded(r"\d+", left_bounds, right_bounds)

        return re.compile(rstr, re.I)

    @classmethod
    def data2entity_list(cls, data):
        logger = FoxylibLogger.func_level2logger(cls.data2entity_list, logging.DEBUG)

        entity_type = TimeEntity.entity_type()

        text_in = TimeEntity.Data.data2text_in(data)
        m_list_hour = TimeEntity.Data.data2match_list_hour(data)
        m_list_minute = TimeEntity.Data.data2match_list_digit_2(data)

        span_list_hour = lmap(lambda m: m.span(), m_list_hour)
        span_list_minute = lmap(lambda m: m.span(), m_list_minute)

        def gap2valid(span):
            str_span = SpanTool.list_span2sublist(text_in, span)
            return RegexTool.pattern_str2match_full(cls.pattern_colon(), str_span)

        def text2entity_list_hm():
            spans_list = [span_list_hour, span_list_minute]

            indextuple_list = ContextfreeTool.spans_list2reducible_indextuple_list(spans_list, gap2valid)

            def indextuple2entity(indextuple):
                i, j = indextuple
                span = (span_list_hour[i][0], span_list_minute[j][1])
                m1, m2 = m_list_hour[i], m_list_minute[j]
                hour, minute = int(m1.group()), int(m2.group())

                # logger.debug({"hour": hour, "minute": minute,
                #               "TimeTool.hour2is_valid(hour)":TimeTool.hour2is_valid(hour),
                #               })
                if not TimeTool.hour2is_valid(hour):
                    return None

                if not TimeTool.minute2is_valid(minute):
                    return None

                value = {TimeEntity.Value.Field.HOUR: hour,
                         TimeEntity.Value.Field.MINUTE: minute,
                         }

                entity = {FoxylibEntity.Field.TYPE: entity_type,
                          FoxylibEntity.Field.FULLTEXT: text_in,
                          FoxylibEntity.Field.SPAN: span,
                          FoxylibEntity.Field.VALUE: value,
                          }
                return entity

            entity_list = lfilter(bool, map(indextuple2entity, indextuple_list))
            # logger.debug({"entity_list": entity_list,
            #               "indextuple_list":indextuple_list,
            #               })

            return entity_list

        def text2entity_list_hms():
            entity_list_hm = text2entity_list_hm()
            span_list_hm = lmap(FoxylibEntity.entity2span, entity_list_hm)
            span_list_second = span_list_minute
            spans_list = [span_list_hm, span_list_second]

            indextuple_list = ContextfreeTool.spans_list2reducible_indextuple_list(spans_list, gap2valid)
            h_i2j = dict(indextuple_list)

            def i2entity(i):
                if i not in h_i2j:
                    return entity_list_hm[i]

                j = h_i2j[i]

                span = (span_list_hm[i][0], span_list_second[j][1])
                entity_hm, m2 = entity_list_hm[i], span_list_second[j]
                value_hm = FoxylibEntity.entity2value(entity_hm)

                hour, minute = TimeEntity.Value.value2hm(value_hm)
                second = int(m2.group())

                if not TimeTool.second2is_valid(second):
                    return None

                value = {TimeEntity.Value.Field.HOUR: hour,
                         TimeEntity.Value.Field.MINUTE: minute,
                         TimeEntity.Value.Field.SECOND: second,
                         }

                entity = {FoxylibEntity.Field.TYPE: entity_type,
                          FoxylibEntity.Field.FULLTEXT: text_in,
                          FoxylibEntity.Field.SPAN: span,
                          FoxylibEntity.Field.VALUE: value,
                          }
                return entity

            return lmap(i2entity, range(len(entity_list_hm)))

        entity_list_hms = text2entity_list_hms()
        entity_list_ampm = TimeEntity.entity_list2ampm_suffixed(data, entity_list_hms)

        return entity_list_ampm
