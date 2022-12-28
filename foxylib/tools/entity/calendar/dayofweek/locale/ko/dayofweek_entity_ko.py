import logging
import re
from functools import lru_cache
from itertools import chain

from future.utils import lmap

from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts, lchain, luniq

from foxylib.tools.entity.calendar.dayofweek.dayofweek_entity import DayofweekEntity
from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool, rstr2wrapped
from foxylib.tools.string.string_tool import format_str


class DayofweekEntityKo:
    @classmethod
    def h_value2str(cls):
        return {DayofweekEntity.V.MONDAY:"월",
                DayofweekEntity.V.TUESDAY: "화",
                DayofweekEntity.V.WEDNESDAY: "수",
                DayofweekEntity.V.THURSDAY: "목",
                DayofweekEntity.V.FRIDAY: "금",
                DayofweekEntity.V.SATURDAY: "토",
                DayofweekEntity.V.SUNDAY: "일",
                }

    @classmethod
    def _h_str2value(cls):
        return merge_dicts([{s: v}
                            for v, s in cls.h_value2str().items()],
                           vwrite=vwrite_no_duplicate_key)

    @classmethod
    def str2value(cls, s):
        h = cls._h_str2value()
        return h.get(s)

    @classmethod
    def rstr_short(cls):
        h = cls.h_value2str()
        return RegexTool.rstrs2or(h.values())




    @classmethod
    def text2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.text2entity_list, logging.DEBUG)

        entity_list_single = DayofweekEntityKoSingle.text2entity_list(str_in)
        entity_list_concat = DayofweekEntityKoConcat.text2entity_list(str_in)
        ll = [entity_list_single, entity_list_concat,]
        l = sorted(luniq(chain(*ll), idfun=FoxylibEntity.entity2span), key=FoxylibEntity.entity2span)

        logger.debug({"entity_list_single": entity_list_single,
                      "entity_list_concat":entity_list_concat,
                      "ll":ll,
                      "l":l,
                      })

        return l


class DayofweekEntityKoSingle:
    @classmethod
    def rstr(cls):
        return format_str(r"{}(?:요일)?", rstr2wrapped(DayofweekEntityKo.rstr_short()))

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern(cls):
        return re.compile(RegexTool.rstr2wordbounded(cls.rstr()), re.I)

    @classmethod
    def text2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.text2entity_list, logging.DEBUG)
        p = cls.pattern()
        m_list = list(p.finditer(str_in))

        def match2entity(m):
            text = m.group()
            v = DayofweekEntityKo.str2value(text[:1])
            return {FoxylibEntity.Field.SPAN: m.span(),
                    FoxylibEntity.Field.VALUE: v,
                    FoxylibEntity.Field.FULLTEXT: str_in,
                    FoxylibEntity.Field.TYPE: DayofweekEntity.entity_type(),
                    FoxylibEntity.Field.TEXT: text,
                    }

        return lmap(match2entity, m_list)


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
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern(cls):
        return re.compile(RegexTool.rstr2wordbounded(cls.rstr()), re.I)

    @classmethod
    def text2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.text2entity_list, logging.DEBUG)
        p = cls.pattern()
        m_list = list(p.finditer(str_in))
        logger.debug({"m_list": m_list,})

        def match2entity_list(m):
            s, e = m.span()
            text = m.group()
            n = len(text)

            l = [{FoxylibEntity.Field.SPAN: (s + i, s + i + 1),
                  FoxylibEntity.Field.VALUE: DayofweekEntityKo.str2value(text[i]),
                  FoxylibEntity.Field.TEXT: text[i],
                  FoxylibEntity.Field.FULLTEXT: str_in,
                  FoxylibEntity.Field.TYPE: DayofweekEntity.entity_type(),
                  }
                 for i in range(n)
                 if text[i] != "," and not text[i].isspace()]

            # logger.debug({"s": s,
            #               "e": e,
            #               "m": m,
            #               "text": text,
            #               "n": n,
            #               "l": l,
            #               })
            return l

        return lchain(*lmap(match2entity_list, m_list))
