import re
from functools import lru_cache

from foxylib.tools.collections.collections_tool import lchain
from future.utils import lfilter, lmap

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.entity.calendar.hms.hour_entity import HourEntity
from foxylib.tools.entity.cardinal.cardinal_entity import CardinalEntity
from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.nlp.contextfree.contextfree_tool import ContextfreeTool
from foxylib.tools.regex.regex_tool import RegexTool, MatchTool
from foxylib.tools.string.string_tool import StringTool


class HourEntityKo:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern_suffix(cls):

        left_bounds = RegexTool.left_wordbounds()
        right_bounds = lchain(RegexTool.right_wordbounds(),
                              [RegexTool.bound2prefixed(b, r"시") for b in RegexTool.right_wordbounds()],
                              )

        rstr_rightbounded = RegexTool.rstr2right_bounded(r"\d+", right_bounds)


        def bound_iter_left():
            b_list_raw = RegexTool.left_wordbounds()
            for b in b_list_raw:
                yield b
                yield r"{}{}".format(b, r"{1,2}")

        bound_list_left = list(bound_iter_left())
        rstr_bound = RegexTool.rstr2left_bounded(rstr_rightbound, bound_list_left)

        return re.compile(rstr_bound)


    @classmethod
    @IterTool.f_iter2f_list
    def text2entity_list(cls, str_in, config=None):
        def entity2is_wordbound_prefixed(entity):
            return StringTool.str_span2is_wordbound_prefixed(str_in, FoxylibEntity.entity2span(entity))

        cardinal_entity_list = lfilter(entity2is_wordbound_prefixed, CardinalEntity.text2entity_list(str_in))

        m_list_suffix = cls.pattern_suffix().finditer(str_in)

        span_ll = [lmap(FoxylibEntity.entity2span, cardinal_entity_list),
                   lmap(MatchTool.match2span, m_list_suffix),
                   ]

        f_span2is_gap = lambda span: StringTool.str_span2match_blank_or_nullstr(str_in, span,)
        j_tuple_list = ContextfreeTool.spans_list2reducible_indextuple_list(span_ll, f_span2is_gap)

        for j1, j2 in j_tuple_list:
            cardinal_entity = cardinal_entity_list[j1]
            m_suffix = m_list_suffix[j2]

            span = (FoxylibEntity.entity2span(cardinal_entity)[0], MatchTool.match2span(m_suffix)[1])
            j_entity = {FoxylibEntity.Field.TYPE: HourEntity.entity_type(),
                        FoxylibEntity.Field.SPAN: span,
                        FoxylibEntity.Field.FULLTEXT: str_in,
                        FoxylibEntity.Field.VALUE: FoxylibEntity.entity2value(cardinal_entity),
                        }
            yield j_entity
