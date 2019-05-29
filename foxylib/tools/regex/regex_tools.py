import re
from functools import lru_cache

from future.utils import lmap, lfilter

from foxylib.tools.collections.collections_tools import l_singleton2obj
from foxylib.tools.string.string_tools import format_str


class RegexToolkit:
    @classmethod
    def str_list2rstr_or(cls, l):
        return r"|".join(lmap(re.escape, l))

    @classmethod
    def rstr2rstr_words_prefixed(cls, rstr, rstr_prefix=None, ):
        # \b (word boundary)_does not work when str_query quoted or double-quoted
        # might wanna use string matching than regex because of speed issue
        rstr_pre = r"(?:(?<=^{0})|(?<=\s{0})|(?<=\b{0}))".format(rstr_prefix or "")
        return r'{0}(?:{1})'.format(rstr_pre, rstr, )

    @classmethod
    def rstr2rstr_words_suffixed(cls, rstr, rstr_suffix=None, ):
        # \b (word boundary)_does not work when str_query quoted or double-quoted
        # might wanna use string matching than regex because of speed issue
        rstr_suf = r"(?=(?:{0})(?:\s|\b|$))".format(rstr_suffix or "")
        return r'(?:{0}){1}'.format(rstr, rstr_suf)

    @classmethod
    def rstr2rstr_words(cls, rstr, rstr_prefix=None, rstr_suffix=None, ):
        # \b (word boundary)_does not work when str_query quoted or double-quoted
        # might wanna use string matching than regex because of speed issue

        rstr_prefixed = cls.rstr2rstr_words_prefixed(rstr, rstr_prefix=rstr_prefix)
        rstr_words = cls.rstr2rstr_words_suffixed(rstr_prefixed, rstr_suffix=rstr_suffix)
        return rstr_words

    @classmethod
    def rstr2rstr_line_prefixed(cls, rstr, rstr_prefix=None,):
        rstr_pre = r"(?:(?<=^{0})|(?<=\n{0}))".format(rstr_prefix or "")
        return r'{0}(?:{1})'.format(rstr_pre, rstr)

    @classmethod
    def rstr2rstr_line_suffixed(cls, rstr, rstr_suffix=None, ):
        rstr_suf = r"(?=(?:{0})(?:\n|$))".format(rstr_suffix or "")
        return r'(?:{}){}'.format(rstr, rstr_suf)

    @classmethod
    def rstr2rstr_line(cls, rstr, rstr_prefix=None, rstr_suffix=None, ):
        rstr_prefixed = cls.rstr2rstr_line_prefixed(rstr, rstr_prefix=rstr_prefix)
        rstr_line = cls.rstr2rstr_line_suffixed(rstr_prefixed, rstr_suffix=rstr_suffix)
        return rstr_line

    @classmethod
    def join(cls, delim, iterable):
        rstr_list_padded = map(lambda s: r"(?:{0})".format(s), iterable)
        return r"(?:{0})".format(delim.join(rstr_list_padded))

    @classmethod
    def name_rstr2rstr(cls, name, rstr):
        return format_str(r"(?P<{0}>{1})", name, rstr)

    @classmethod
    @lru_cache(maxsize=2)
    def pattern_blank(cls):
        return re.compile("\s+")


    @classmethod
    def p_str2m_uniq(cls, pattern, s):
        m_list = list(pattern.finditer(s))
        if not m_list: return None

        m = l_singleton2obj(m_list)
        return m

    @classmethod
    def rstr2rstr_last(cls, rstr):
        return r"(?:{})(?!.*(?:{}))".format(rstr)

class MatchToolkit:
    @classmethod
    def i2m_right_before(cls, i, m_list):
        if not m_list:
            return None

        m_list_valid = lfilter(lambda m: m.end() <= i, m_list)
        if not m_list_valid: return None

        m_max = max(m_list_valid, key=lambda m: m.start())
        return m_max

    @classmethod
    def match2se(cls, m):
        return m.span()

    @classmethod
    def match2span(cls, m):
        return cls.match2se(m)

    @classmethod
    def match2start(cls, m):
        return cls.match2se(m)[0]

    @classmethod
    def match2end(cls, m):
        return cls.match2se(m)[1]

    @classmethod
    def match2text(cls, m):
        return m.group()

    @classmethod
    def match2str_group(cls, m):
        l = [name for name, value in m.groupdict().items() if value is not None]
        return l_singleton2obj(l)

    @classmethod
    def match2explode(cls, str_in, m):
        if not m: return str_in

        s,e = MatchToolkit.match2span(m)
        t = (str_in[:s], str_in[s:e], str_in[e:])
        return t

