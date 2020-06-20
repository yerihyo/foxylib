import logging
import re
from functools import lru_cache

from future.utils import lmap, lfilter

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.collections.collections_tool import merge_dicts, lchain, \
    vwrite_overwrite, tmap
from foxylib.tools.entity.calendar.dayofweek.dayofweek_span_entity import DayofweekSpanEntity
from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo, \
    DayofweekEntityKoSingle
from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.nlp.contextfree.contextfree_tool import ContextfreeTool
from foxylib.tools.regex.regex_tool import RegexTool, MatchTool
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.string_tool import StringTool


class DayofweekSpanEntityKo:
    @classmethod
    def rstr_delim(cls):
        return r"[-~]"

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_delim(cls):
        return re.compile(RegexTool.rstr2rstr_words(cls.rstr_delim()), re.I)



    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=256))
    def str_span2is_gap(cls, str_in, span):
        return StringTool.str_span2match_blank_or_nullstr(str_in, span)

    @classmethod
    @IterTool.f_iter2f_list
    def _text2entity_list_multiday(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls._text2entity_list_multiday, logging.DEBUG)

        entity_list_1day = DayofweekEntityKoSingle.text2entity_list(str_in)


        p_delim = cls.pattern_delim()
        m_list_delim = list(p_delim.finditer(str_in))

        span_ll = [lmap(FoxylibEntity.entity2span, entity_list_1day),
                   lmap(MatchTool.match2span, m_list_delim),
                   lmap(FoxylibEntity.entity2span, entity_list_1day),
                   ]

        f_span2is_gap = lambda span: cls.str_span2is_gap(str_in, span)
        j_tuple_list = list(ContextfreeTool.spans_list2reducible_indextuple_list(span_ll,f_span2is_gap))

        logger.debug({"j_tuple_list":j_tuple_list,
                      "entity_list_1day":entity_list_1day,
                      "m_list_delim":m_list_delim,
                      })

        for j_tuple in j_tuple_list:
            j1, j2, j3 = j_tuple

            entity_pair = entity_list_1day[j1], entity_list_1day[j3]
            logger.debug({"j1": j1,
                          "j3": j3,
                          "entity_pair": entity_pair,
                          })

            span = (FoxylibEntity.entity2span(entity_pair[0])[0],
                    FoxylibEntity.entity2span(entity_pair[1])[1],
                    )
            j_entity = {FoxylibEntity.Field.TYPE: DayofweekSpanEntity.entity_type(),
                        FoxylibEntity.Field.SPAN: span,
                        FoxylibEntity.Field.FULLTEXT: str_in,
                        FoxylibEntity.Field.VALUE: tmap(FoxylibEntity.entity2value, entity_pair),
                        }
            yield j_entity

    @classmethod
    def _entity_1day2multiday(cls, j_entity_1day):
        v_1day = FoxylibEntity.entity2value(j_entity_1day)

        j_entity_multiday = merge_dicts([j_entity_1day,
                                         {FoxylibEntity.Field.VALUE: (v_1day,)}
                                         ], vwrite=vwrite_overwrite)
        return j_entity_multiday

    @classmethod
    def text2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.text2entity_list, logging.DEBUG)

        entity_list_1day_raw = DayofweekEntityKo.text2entity_list(str_in)

        entity_list_multiday = cls._text2entity_list_multiday(str_in)
        span_list_multiday = lmap(FoxylibEntity.entity2span, entity_list_multiday)

        def entity_1day2is_not_covered(entity_1day):
            span_1day = FoxylibEntity.entity2span(entity_1day)
            for span_multiday in span_list_multiday:
                if SpanTool.covers(span_multiday, span_1day):
                    return False
            return True

        entity_list_1day_uncovered = lfilter(entity_1day2is_not_covered, entity_list_1day_raw)

        entity_list = lchain(lmap(cls._entity_1day2multiday, entity_list_1day_uncovered),
                             entity_list_multiday)

        return entity_list


# class DayofweekSpanEntityKoSpan:
#
#
#
#     @classmethod
#     @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
#     def pattern(cls):
#         return re.compile(RegexTool.rstr2rstr_words(cls.rstr()), re.I)
#
#
#     @classmethod
#     def text2entity_list(cls, str_in):
#         logger = FoxylibLogger.func_level2logger(cls.text2entity_list, logging.DEBUG)
#         p = cls.pattern()
#         m_list = list(p.finditer(str_in))
#
#         # logger.debug({"p": p,
#         #               "m_list": m_list,
#         #               "str_in": str_in,
#         #               })
#
#         return lmap(cls.match2entity, m_list)
#
#
# class DayofweekEntityKoConcat:
#     @classmethod
#     def rstr(cls):
#         rstr_short = DayofweekEntityKo.rstr_short()
#         rstr = format_str("{}(?:(?:\s*,\s*)?{})+",
#                           rstr2wrapped(rstr_short),
#                           rstr2wrapped(rstr_short),
#                           )
#         return rstr
#
#     @classmethod
#     @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
#     def pattern(cls):
#         return re.compile(RegexTool.rstr2rstr_words(cls.rstr()), re.I)
#
#
#
#
#     @classmethod
#     def text2entity_list(cls, str_in):
#         logger = FoxylibLogger.func_level2logger(cls.text2entity_list, logging.DEBUG)
#         p = cls.pattern()
#         m_list = list(p.finditer(str_in))
#
#         logger.debug({"m_list": m_list,})
#
#         return lchain(*lmap(cls.match2entity_list, m_list))
