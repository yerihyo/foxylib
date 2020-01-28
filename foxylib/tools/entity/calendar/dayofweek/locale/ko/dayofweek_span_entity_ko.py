import logging
import re
from functools import lru_cache
from itertools import chain

from future.utils import lmap

from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts, lchain, luniq

from foxylib.tools.entity.calendar.dayofweek.dayofweek_entity import DayofweekEntity
from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo, \
    DayofweekEntityKoSingle
from foxylib.tools.entity.enrtity_tool import Entity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool, rstr2wrapped
from foxylib.tools.string.string_tool import format_str


class DayofweekSpanEntityKo:
    @classmethod
    def rstr_delim(cls):
        return r"[-~]"

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_delim(cls):
        return re.compile(RegexTool.rstr2rstr_words(cls.rstr_delim()), re.I)

    @classmethod
    def rstr(cls):
        rstr_short = DayofweekEntityKo.rstr_short()

        rstr_oneside = format_str(r"{}(?:요일)?",rstr2wrapped(rstr_short))
        rstr = RegexTool.join(r"\s*",
                              [rstr_oneside,
                               cls.rstr_delim(),
                               rstr_oneside,
                               ])
        return rstr



    @classmethod
    def _str2entity_list(cls, str_in):
        p_single = DayofweekEntityKoSingle.pattern()
        m_list_single = list(p_single.finditer(str_in))

        p_delim = cls.pattern_delim()
        m_list_delim = list(p_delim.finditer(str_in))

        p_blank = RegexTool.pattern_blank()
        m_list_blank = list(p_blank.finditer(str_in))





    @classmethod
    def str2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.str2entity_list, logging.DEBUG)

        entity_list_1day = DayofweekEntityKo.str2entity_list(str_in)

        ll = [entity_list_single, entity_list_concat,]
        l = sorted(luniq(chain(*ll), idfun=Entity.j2span), key=Entity.j2span)

        logger.debug({"entity_list_single": entity_list_single,
                      "entity_list_concat":entity_list_concat,
                      "ll":ll,
                      "l":l,
                      })

        return l


class DayofweekSpanEntityKoSpan:



    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern(cls):
        return re.compile(RegexTool.rstr2rstr_words(cls.rstr()), re.I)

    @classmethod
    def match2entity(cls, m):
        text = m.group()
        v = DayofweekEntityKo.str2value(text[:1])
        return {Entity.F.SPAN: m.span(),
                Entity.F.VALUE: v,
                Entity.F.TEXT: text,
                }

    @classmethod
    def str2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.str2entity_list, logging.DEBUG)
        p = cls.pattern()
        m_list = list(p.finditer(str_in))

        # logger.debug({"p": p,
        #               "m_list": m_list,
        #               "str_in": str_in,
        #               })

        return lmap(cls.match2entity, m_list)


class DayofweekEntityKoConcat:
    @classmethod
    def rstr(cls):
        rstr_short = DayofweekEntityKo.rstr_short()
        rstr = format_str("{}(?:(?:\s*,\s*)?{})+",
                          rstr2wrapped(rstr_short),
                          rstr2wrapped(rstr_short),
                          )
        return rstr

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern(cls):
        return re.compile(RegexTool.rstr2rstr_words(cls.rstr()), re.I)


    @classmethod
    def match2entity_list(cls, m):
        logger = FoxylibLogger.func_level2logger(cls.str2entity_list, logging.DEBUG)

        s,e = m.span()
        text = m.group()
        n = len(text)

        l = [{Entity.F.SPAN: (s + i, s + i + 1),
              Entity.F.VALUE: DayofweekEntityKo.str2value(text[i]),
              Entity.F.TEXT: text[i],
              }
             for i in range(n)
             if text[i]!="," and not text[i].isspace()]

        logger.debug({"s":s,
                      "e":e,
                      "m":m,
                      "text":text,
                      "n":n,
                      "l":l,
                      })
        return l


    @classmethod
    def str2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.str2entity_list, logging.DEBUG)
        p = cls.pattern()
        m_list = list(p.finditer(str_in))

        logger.debug({"m_list": m_list,})

        return lchain(*lmap(cls.match2entity_list, m_list))
