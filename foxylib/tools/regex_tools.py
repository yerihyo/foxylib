import re
from future.utils import lmap


class RegexToolkit:
    @classmethod
    def str_list2rstr_or(cls, l):
        return r"|".join(lmap(re.escape, l))

    @classmethod
    def rstr2rstr_boundered(cls, rstr):
        return r'(?:(?<=^)|(?<=\s)|(?<=\b))(?:{0})(?=\s|\b|$)'.format(rstr)

    @classmethod
    def str_WORD_list2rstr_boundered(cls, l,):
        rstr_flexible_blank = r"\s+".join(lmap(re.escape, l))
        rstr_boundered = cls.rstr2rstr_boundered(rstr_flexible_blank)
        return rstr_boundered

    @classmethod
    def match2span(cls, m): return m.span()

    @classmethod
    def match2text(cls, m): return m.group()

