import re
from functools import lru_cache

from future.utils import lfilter, lmap

from foxylib.tools.collections.collections_tool import f_iter2f_list
from foxylib.tools.entity.cardinal.cardinal_entity import CardinalEntity
from foxylib.tools.entity.entity_tool import Entity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool, MatchTool, p_blank_or_nullstr
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.string_tool import StringTool


class HourEntityKo:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_suffix(cls):
        rstr = RegexTool.rstr2rstr_words_suffixed("시")
        return re.compile(rstr)


    @classmethod
    @f_iter2f_list
    def str2entity_list(cls, str_in, config=None):

        def entity2is_wordbound_prefixed(entity):
            return StringTool.str_span2is_wordbound_prefixed(str_in, Entity.j2span(entity))

        cardinal_entity_list = lfilter(entity2is_wordbound_prefixed, CardinalEntity.str2entity_list(str_in))

        m_list_suffix = cls.pattern_suffix().finditer(str_in)

        span_ll = [lmap(Entity.j2span, cardinal_entity_list),
                   lmap(MatchTool.match2span, m_list_suffix),
                   ]

        f_span2is_gap = lambda span: StringTool.str_span2is_blank_or_nullstr(str_in, span,)
        j_tuple_list = SpanTool.spans_list_f_gap2j_tuples_valid(span_ll, f_span2is_gap)

        for j1, j2 in j_tuple_list:
            cardinal_entity = cardinal_entity_list[j1]
            m_suffix = m_list_suffix[j2]

            span = (Entity.j2span(cardinal_entity)[0], MatchTool.match2span(m_suffix)[1])
            j_entity = {Entity.F.SPAN: span,
                        Entity.F.TEXT: StringTool.str_span2str(str_in, span),
                        Entity.F.VALUE: Entity.j2value(cardinal_entity),
                        }
            yield j_entity
