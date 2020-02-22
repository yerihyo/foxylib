import os
import re
from functools import lru_cache

from future.utils import lmap

from foxylib.tools.entity.entity_tool import Entity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class CardinalEntity:

    @classmethod
    def rstr(cls):
        rstr_multidigit = r"[1-9][0-9]+"
        rstr_onedigit = r"[0-9]"
        rstr_number = RegexTool.rstr_list2or([rstr_multidigit, rstr_onedigit])

        return rstr_number

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern(cls):
        return re.compile(cls.rstr(), re.I)

    @classmethod
    def m2entity(cls, m):
        text = m.group()
        return {Entity.Field.SPAN: m.span(),
                Entity.Field.TEXT: text,
                Entity.Field.VALUE: int(text),
                }


    @classmethod
    def str2entity_list(cls, str_in):
        p = cls.pattern()

        m_list = list(p.finditer(str_in))
        entity_list = lmap(cls.m2entity, m_list)
        return entity_list

