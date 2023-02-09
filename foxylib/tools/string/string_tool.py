import ast
import random
import re
from functools import reduce
from operator import itemgetter as ig
from typing import List

from future.utils import lmap
from nose.tools import assert_false

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.span.indexspan_tool import IndexspanTool
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.version.version_tool import VersionTool


class StringTool:
    @classmethod
    def length2random_str(cls, characters, n):
        return ''.join(random.choices(characters, k=n))

    @classmethod
    def str_spans2replace_all(cls, text_in, span_sub_list):
        span_sub_list_sorted = sorted(span_sub_list, key=ig(0))
        span_list = lmap(ig(0), span_sub_list_sorted)
        assert_false(SpanTool.overlaps_any(span_list), {"spans overlapping": span_list})

        text_out = reduce(lambda text, span_value: StringTool.str_span2sub(text, span_value[0], span_value[1]),
                          reversed(span_sub_list_sorted),
                          text_in
                          )
        return text_out

    @classmethod
    def equals_casefolded(cls, s1, s2):
        if s1 == s2:
            return True

        if not s1:
            return False

        if not s2:
            return False

        return s1.casefold() == s2.casefold()

    @classmethod
    def pair2cmp(cls, s1, s2):
        if s1 == s2:
            return 0

        if s1 < s2:
            return -1

        if s2 > s1:
            return 1

    @classmethod
    def pair2cmp_casefolded(cls, s1, s2):
        return cls.pair2cmp(s1.casefold(), s2.casefold())

    @classmethod
    def str2strip(cls, s:str)->str:
        return cls.str2stripped(s)

    @classmethod
    def str2stripped(cls, s):
        return s.strip() if s else s

    @classmethod
    def str2stripped_eachline(cls, s):
        if not s:
            return s

        return "\n".join(map(cls.str2stripped, s.splitlines()))

    @classmethod
    def str2rstrip(cls, s):
        return s.rstrip() if s else s

    @classmethod
    def str2splitlines(cls, s):
        return s.splitlines() if s else s

    @classmethod
    def str2lower(cls, s):
        return s.lower() if s else s

    @classmethod
    def str2upper(cls, s):
        return s.upper() if s else s

    @classmethod
    def str2casefold(cls, s):
        return s.casefold() if s else s

    @classmethod
    def funcs_cond2func_samelength(cls, funcs):
        def f_cond(s_out, s_in):
            return len(s_out) == len(s_in)

        return FunctionTool.funcs_cond2compiled(funcs, f_cond)

    @classmethod
    def str2lower_samelength(cls, str_in):
        def f_cond(s1, s2):
            return len(s1) == len(s2)

        str2lower_if_samelength = \
            FunctionTool.funcs_cond2compiled([cls.str2lower], f_cond)

        def str2lower_eachchar(s):
            return "".join(lmap(str2lower_if_samelength, s))

        funcs = [cls.str2lower,
                 str2lower_eachchar,
                 ]
        f_compiled = FunctionTool.funcs_cond2compiled(funcs, f_cond)
        return f_compiled(str_in)

    @classmethod
    def str2upper(cls, s):
        return s.upper() if s else s

    @classmethod
    def join_str(cls, s, *_, **__):
        return s.join(*_, **__) if s is not None else s

    @classmethod
    def format_str(cls, s, *_, **__):
        return s.format(*_, **__) if s is not None else s

    @classmethod
    def continuous_blank_lines2removed(cls, str_in, blank_line_count_allowed):

        l_line = lmap(cls.str2stripped, str_in.splitlines())
        i_list_invalid = IterTool.list_func_count2index_list_continuous_valid(l_line, lambda x:not x, blank_line_count_allowed)
        n = len(l_line)

        # raise Exception({"i_list_invalid":i_list_invalid, "l_line":l_line,})
        return "\n".join(lmap(lambda i:l_line[i], filter(lambda i:i not in i_list_invalid, range(n))))


    @classmethod
    def str_span_pattern2match_full(cls, str_in, span, pattern):
        from foxylib.tools.regex.regex_tool import RegexTool
        str_sub = cls.str_span2substr(str_in, span)
        if str_sub is None:
            return None

        m = RegexTool.pattern_str2match_full(pattern, str_sub)
        return m

    @classmethod
    def str_span2match_blank(cls, str_in, span):
        from foxylib.tools.regex.regex_tool import RegexTool
        return cls.str_span_pattern2match_full(str_in, span, RegexTool.pattern_blank())

    @classmethod
    def str_span2match_blank_or_nullstr(cls, str_in, span):
        from foxylib.tools.regex.regex_tool import RegexTool
        return cls.str_span_pattern2match_full(str_in, span, RegexTool.pattern_blank_or_nullstr())




    @classmethod
    def quoted2stripped(cls, s_IN, ):
        try:
            module = ast.parse(s_IN)
        except SyntaxError:
            return s_IN

        node_list = module.body
        if len(node_list) != 1: return s_IN

        node_Expr = node_list[0]
        if not isinstance(node_Expr, ast.Expr): return s_IN

        node_Str = node_Expr.value
        if not isinstance(node_Str, ast.Str): return s_IN

        return node_Str.s

    @classmethod
    def newline2space(cls, s):
        if not s: return s
        return s.replace('\n', ' ').replace('\r', '')

    @classmethod
    def str_span2substr(cls, str_in, span):
        return IndexspanTool.list_span2sublist(str_in, span)

    @classmethod
    def str2split(cls, s, *args, **kwargs) -> List[str]:
        return s.split(*args, **kwargs) if s is not None else s

    @classmethod
    def str2split_n_eachstripped(cls, s, *_, **__) -> List[str]:
        return lmap(cls.str2stripped, s.split(*_, **__)) if s is not None else s

    @classmethod
    def escape_quotes(cls, s):
        return s.replace('"', '\\"').replace("'", "\\'")

    @classmethod
    def escape_doublequotes(cls, s):
        return s.replace('"', '\\"')

    @classmethod
    def query2indices(cls, s_query, s_doc):
        start = 0
        while True:

            i = s_doc.find(s_query, start)
            if i < 0: break

            yield i
            start = i+1

    @classmethod
    def span2strip(cls, ipair, str_in):
        if not ipair:
            return ipair

        s, e = ipair

        s_match = str_in[s:e]
        s_strip = s_match.strip()

        i_start = s_match.find(s_strip)

        s_out = s + i_start
        e_out = s_out + len(s_strip)

        return (s_out, e_out)

    @classmethod
    def str_spans_func2processed(cls, str_in, span_list, func,):
        from foxylib.tools.span.span_tool import SpanTool
        str_out = SpanTool.list_spans_func2processed(str_in, span_list, func, f_list2chain="".join)
        return str_out

    @classmethod
    def whitespace2stripped(cls, str_in):
        return "".join(str_in.split())

    @classmethod
    def str2is_pound_comment(cls, str_in):
        if not str_in: return False

        return str_in.strip().startswith("#")

    @classmethod
    def str2has_none_whitespace(cls, str_in):
        if not str_in: return False
        return (not str_in.isspace())

    @classmethod
    def is_string(cls, x):
        return isinstance(x, str)

    # @classmethod
    # def str_format2escaped(cls, s_format):
    #     return re.sub("{[\w,]+}","{\g<0>}",s_format)

    @classmethod
    def dict2f_sub(cls, h):
        # Create a regular expression from all of the dictionary keys
        from foxylib.tools.regex.regex_tool import RegexTool
        rstr = RegexTool.join(r"|".join(map(re.escape, h.keys())))
        p = re.compile(rstr)

        # For each match, look up the corresponding value in the dictionary
        return lambda x: p.sub(lambda m: h[m.group(0)], x)

    @classmethod
    def str_dict2sub(cls, str_in, h):
        f_sub = cls.dict2f_sub(h)
        return f_sub(str_in)

    @classmethod
    def str_span2sub(cls, str_in, span, str_sub):
        s,e = span
        str_out = "".join([str_in[:s],str_sub,str_in[e:]])
        return str_out

    @classmethod
    def str_span2is_wordbound_prefixed(cls, str_in, span):
        if span[0] == 0:
            return True

        if str_in[span[0] - 1].isalnum():
            return False

        return True

    @classmethod
    def str_span2is_wordbound_suffixed(cls, str_in, span):
        if span[-1] == len(str_in):
            return True

        if str_in[span[-1] + 1].isalnum():
            return False

        return True

    @classmethod
    def str_span2is_wordbounded(cls, str_in, span):
        if not cls.str_span2is_wordbound_prefixed(str_in, span):
            return False

        if not cls.str_span2is_wordbound_suffixed(str_in, span):
            return False

        return True

    @classmethod
    def pattern_camelcase(cls):
        return re.compile(r'(?<!^)(?=[A-Z])')

    @classmethod
    @VersionTool.deprecated(reason='pre-compile pattern in real usage')
    def camelcase2snakecase(cls, camelcase_in:str):
        # https://stackoverflow.com/a/1176023/1902064
        return StringTool.pattern_camelcase().sub('_', camelcase_in).lower()




format_str = StringTool.format_str


str2stripped = StringTool.str2stripped
str2strip = str2stripped

str2rstrip = StringTool.str2rstrip
str2lower = StringTool.str2lower
str2upper = StringTool.str2upper
join_str = StringTool.join_str

str2split = StringTool.str2split
str2splitlines = StringTool.str2splitlines
escape_quotes = StringTool.escape_quotes
escape_doublequotes = StringTool.escape_doublequotes
whitespace2stripped = StringTool.whitespace2stripped
str2has_nw = StringTool.str2has_none_whitespace
str2is_pound_comment = StringTool.str2is_pound_comment
is_string = StringTool.is_string
# str_format2escaped = StringTool.str_format2escaped