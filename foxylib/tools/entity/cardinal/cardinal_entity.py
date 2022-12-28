import os
import re
from functools import lru_cache

from future.utils import lmap

from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class CardinalEntity:

    @classmethod
    def rstr(cls):
        rstr_multidigit = r"[1-9][0-9]+"
        rstr_onedigit = r"[0-9]"
        rstr_number = RegexTool.rstrs2or([rstr_multidigit, rstr_onedigit])

        return rstr_number

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern(cls):
        return re.compile(cls.rstr(), re.I)

    @classmethod
    def text2entity_list(cls, str_in):
        p = cls.pattern()

        m_list = list(p.finditer(str_in))

        def match2entity(m):
            text = m.group()
            return {FoxylibEntity.Field.SPAN: m.span(),
                    FoxylibEntity.Field.TEXT: text,
                    FoxylibEntity.Field.FULLTEXT: str_in,
                    FoxylibEntity.Field.VALUE: int(text),
                    }

        entity_list = lmap(match2entity, m_list)
        return entity_list

