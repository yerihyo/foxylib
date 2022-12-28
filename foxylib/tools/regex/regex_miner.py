import logging
import re
from functools import lru_cache
from itertools import chain
from operator import itemgetter as ig

from future.utils import lmap, lfilter

from foxylib.tools.collections.collections_tool import list2singleton
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool

logger = logging.getLogger(__name__)


class RegexMiner:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern_alpha(cls):
        return re.compile(r"[a-z]", re.I)

    @classmethod
    @lru_cache(maxsize=1)
    def pattern_stackable(cls):
        rstrs = [r"\\[d]",
                 r"\[([-A-Za-z0-9_]+)\]"
                 ]

        rstr_or = RegexTool.rstrs2or(rstrs)
        p = re.compile(RegexTool.rstr2wordbounded(rstr_or))
        return p

    @classmethod
    def rstr2is_stackable(cls, rstr):
        if len(rstr) == 1:
            return True

        p = cls.pattern_stackable()
        return RegexTool.pattern_str2is_fullmatch(p, rstr)

    @classmethod
    def tokens2compressed(cls, tokens_in):
        latest = None

        def latest2flushed(latest_in):
            if latest_in is None:
                return None

            rstr_current, count = latest_in
            if not rstr_current:
                return None

            if count == 1:
                return rstr_current

            if len(rstr_current) == 1 and count <= 3:
                return rstr_current * count

            is_stackable = cls.rstr2is_stackable(rstr_current)
            rstr_base = rstr_current if is_stackable else RegexTool.rstr2wrapped(
                rstr_current)
            rstr_out = rstr_base + '{' + str(count) + '}'

            return rstr_out

        def token2is_appendable(token_in):
            if latest:
                rstr_latest, count_latest = latest
                if token_in != rstr_latest:
                    return False

            if cls.rstr2is_stackable(token_in):
                return True

            return False

        for token_in in tokens_in:
            if not token2is_appendable(token_in):
                if latest:
                    rstr_flushed = latest2flushed(latest)
                    yield rstr_flushed

                latest = token_in, 1

            elif latest is None:
                latest = token_in, 1
            else:
                latest = token_in, latest[1] + 1

        if latest:
            rstr_flushed = latest2flushed(latest)
            yield rstr_flushed

    @classmethod
    def samelengths2regex(cls, texts, thres_char_count=None,):
        n = list2singleton(map(len, texts))

        def char_list2regex(chars_in):
            char_list = list(set(chars_in))
            n = len(char_list)

            if n <= thres_char_count:
                return RegexTool.rstrs2or(map(re.escape, char_list))

            i_list_digit = lfilter(lambda i: char_list[i].isdigit(), range(n))
            if len(i_list_digit) == n:
                return r"\d"

            i_list_alpha = lfilter(lambda i: cls.pattern_alpha().match(char_list[i]), range(n))
            if len(i_list_alpha) == n:
                return r"[a-zA-Z]"

            if len(set(chain(i_list_alpha, i_list_digit))) == n:
                return r"[a-zA-Z0-9]"

            return r"."

        rstr_list = [char_list2regex(lmap(ig(i), texts))
                     for i in range(n)]

        rstr = r"".join(cls.tokens2compressed(rstr_list))
        return rstr
