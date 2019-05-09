import re
from future.utils import lmap

from foxylib.tools.collections.collections_tools import l_singleton2obj


class RegexToolkit:
    @classmethod
    def str_list2rstr_or(cls, l):
        return r"|".join(lmap(re.escape, l))


    @classmethod
    def rstr2rstr_b(cls, rstr):
        return r'(?:(?<=^)|(?<=\s)|(?<=\b))(?:{0})(?=\s|\b|$)'.format(rstr)
    @classmethod
    def rstr2rstr_boundered(cls, rstr): return cls.rstr2rstr_b(rstr)

    @classmethod
    def str_WORD_list2rstr_boundered(cls, l,):
        rstr_flexible_blank = r"\s+".join(lmap(re.escape, l))
        rstr_b = cls.rstr2rstr_b(rstr_flexible_blank)
        return rstr_b

    @classmethod
    def match2span(cls, m): return m.span()

    @classmethod
    def match2text(cls, m): return m.group()


    @classmethod
    def p_str2m_uniq(cls, pattern, s):
        m_list = list(pattern.finditer(s))
        if not m_list: return None

        m = l_singleton2obj(m_list)
        return m

    @classmethod
    def p_pair_str2m_uniq(cls, p_begin, p_end, s):
        m_begin = cls.p_str2m_uniq(p_begin, s)


        m_list = list(p_begin.finditer(s))
        m = l_singleton2obj(m_list)
        return m