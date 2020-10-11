import re
from functools import lru_cache

from foxylib.tools.collections.collections_tool import lchain, merge_dicts, vwrite_no_duplicate_key
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool


class UnicodeTool:
    @classmethod
    def utf82surrogate_escaped(cls, utf8):
        # https://github.com/elastic/elasticsearch-py/issues/611
        return utf8.encode('utf-8', "backslashreplace").decode('utf-8')

    @classmethod
    def lstrip_bom(cls, text):
        return text.lstrip('\ufeff')

    @classmethod
    def string_singlequote(cls):
        return "`´‘’'"

    @classmethod
    def string_doublequote(cls):
        return '“”"'

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_variation(cls):
        l = lchain(cls.string_singlequote(), cls.string_doublequote())
        rstr = RegexTool.rstr_iter2or(map(re.escape,l))
        p = re.compile(rstr)
        return p

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def h_char2typable(cls):
        h = merge_dicts([{c: "'" for c in cls.string_singlequote()},
                         {c: '"' for c in cls.string_doublequote()},
                         ], vwrite=vwrite_no_duplicate_key)
        return h

    @classmethod
    def str2typable(cls, str_in):
        p = cls.pattern_variation()

        h = cls.h_char2typable()
        str_out = p.sub(lambda m: h[m.group()], str_in)
        return str_out


