import re
from functools import lru_cache

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import StringTool


class EnglishSimpleTokenizer:
    """
    Alternative for Spacy's string tokenizer due to speed issue
    """

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def _pattern_blank(cls):
        return re.compile(r'[-\s]+')

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def _pattern_token(cls):
        """
        n't is specially treated because if we split by word boundary, the tokens/morphemes don't make sense.

        e.g. don't => don / ' / t   ("don" is not a valid token/morpheme)
        e.g. jane's => jane / ' / s  ("jean", "'", "s" are all valid morpheme)

        correct morphology
        e.g. don't => do / n't  (however we don't need to go this far.
                                 treating don't as a single token ok for most purposes.)
        """
        rstr = RegexTool.join(r"|", [r"\w+(?:n't)", r"\w+", r"\W+"])
        return re.compile(RegexTool.rstr2wrapped(rstr))
        # return re.compile(r'[-\s]+')

    @classmethod
    def str2token_span_list(cls, str_in):
        p_token = cls._pattern_token()
        m_list_all = list(p_token.finditer(str_in))

        p_blank = cls._pattern_blank()
        m_list_nowhitespace = filter(lambda m: not RegexTool.pattern_str2match_full(p_blank, m.group()),
                                     m_list_all)
        span_list = [m.span() for m in m_list_nowhitespace]
        return span_list

    @classmethod
    def str2token_list(cls, str_in):
        span_list = cls.str2token_span_list(str_in)
        return [StringTool.str_span2substr(str_in, span) for span in span_list]
