import os
from functools import partial

from foxylib.tools.native.native_tool import is_not_none
from future.utils import lmap, lfilter

from foxylib.tools.datetime.datetime_tool import TimeTool
from foxylib.tools.entity.calendar.time.time_entity import AMPM, TimeEntity
from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.nlp.contextfree.contextfree_tool import ContextfreeTool
from foxylib.tools.string.string_tool import StringTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class HourAMPMTimeEntity:
    @classmethod
    def data2entity_list(cls, data):
        text_in = TimeEntity.Data.data2text_in(data)

        m_list_hour = TimeEntity.Data.data2match_list_digit_1or2(data)
        span_list_hour = lmap(lambda m: m.span(), m_list_hour)

        m_list_ampm = TimeEntity.Data.data2match_list_ampm(data)
        span_list_ampm = lmap(lambda m: m.span(), m_list_ampm)

        spans_list = [span_list_hour, span_list_ampm,]
        gap2is_valid = partial(StringTool.str_span2match_blank_or_nullstr, text_in)
        indextuple_list = ContextfreeTool.spans_list2reducible_indextuple_list(spans_list, gap2is_valid)

        def indextuple2entity(indextuple):
            i, j = indextuple
            m_hour, m_ampm = m_list_hour[i], m_list_ampm[j]

            hour_raw = TimeTool.hour2norm(int(m_hour.group()))
            if hour_raw is None:
                return None

            hour, ampm = AMPM.hour_ampm2normalized(hour_raw, AMPM.match2value(m_ampm))
            if hour is None:
                return None

            if ampm is None:
                return None

            span = (m_hour.span()[0], m_ampm.span()[1])
            value = {TimeEntity.Value.Field.HOUR: hour,
                     TimeEntity.Value.Field.MINUTE: 0,
                     TimeEntity.Value.Field.AMPM: ampm,
                     }
            entity = {FoxylibEntity.Field.FULLTEXT: text_in,
                      FoxylibEntity.Field.TYPE: TimeEntity.entity_type(),
                      FoxylibEntity.Field.SPAN: span,
                      FoxylibEntity.Field.VALUE: value
                      }
            return entity

        entity_list = lfilter(is_not_none, map(indextuple2entity, indextuple_list))
        return entity_list


