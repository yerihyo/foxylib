import ast
import re
from itertools import product
from operator import itemgetter as ig

from foxylib.tools.collections.groupby_tool import h_gb_tree
from future.utils import lmap, lfilter
from nose.tools import assert_greater_equal

from foxylib.tools.collections.collections_tool import IterTool, tchain
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool


class StringTool:
    @classmethod
    def str2strip(cls, s):
        return s.strip() if s else s

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
    def join_str(cls, s, *args, **kwargs):
        return s.join(*args, **kwargs) if s else s


    @classmethod
    def format_str(cls, s, *args, **kwargs):
        logger = FoxylibLogger.func2logger(cls.format_str)
        if not s: return s

        # logger.debug({"s":s,"args":args, "kwargs":kwargs})
        return s.format(*args, **kwargs)

    @classmethod
    def continuous_blank_lines2removed(cls, str_in, blank_line_count_allowed):

        l_line = lmap(cls.str2strip, str_in.splitlines())
        i_list_invalid = IterTool.list_func_count2index_list_continuous_valid(l_line, lambda x:not x, blank_line_count_allowed)
        n = len(l_line)

        # raise Exception({"i_list_invalid":i_list_invalid, "l_line":l_line,})
        return "\n".join(lmap(lambda i:l_line[i], filter(lambda i:i not in i_list_invalid, range(n))))

    # @classmethod
    # def str_span_pair2is_deliminated(cls, str_in, span_pair, p_delim):
    #     span1, span2 = span_pair
    #     s, e = span1[1], span2[0]
    #
    #     if s > e:
    #         return False
    #
    #     from foxylib.tools.regex.regex_tool import RegexTool
    #     m = RegexTool.pattern_str2match_full(p_delim, str_in[s:e])
    #     is_deliminated = (m is not None)
    #     return is_deliminated

    # @classmethod
    # def str_spans_pair2j_pairs_deliminated(cls, str_in, spans_pair, p_delim):
    #     def span_pair2is_valid(span1, span2):
    #         return cls.str_span_pair2is_deliminated(str_in, (span1, span2), p_delim)
    #
    #     spans1, spans2 = spans_pair
    #     p1, p2 = len(spans1), len(spans2)
    #
    #     for j1, j2 in product(range(p1), range(p2)):
    #         if span_pair2is_valid(spans1[j1], spans2[j2]):
    #             yield (j1, j2)

    # @classmethod
    # def str_spans_list2h_lookup_deliminated(cls, str_in, spans_list, p_delim):
    #     span_pair_set = set((span1[1], span2[0])
    #                         for spans1, spans2 in IterTool.iter2pair_iter(spans_list)
    #                         for span1, span2 in product(spans1, spans2))
    #
    #     h = {span_pair: StringTool.str_span_pattern2match_full(str_in, span_pair, p_delim)
    #          for span_pair in span_pair_set}
    #     return h

    # @classmethod
    # def spans_list_lookup2j_tuples_valid(cls, spans_list, h_span_pair2is_valid):
    #     assert_greater_equal(len(spans_list), 2)
    #
    #     def spans_pair2j_pairs_deliminated(spans_pair, ):
    #         spans1, spans2 = spans_pair
    #         p1, p2 = len(spans1), len(spans2)
    #
    #         for j1, j2 in product(range(p1), range(p2)):
    #             span_pair = (tuple(spans1[j1]), tuple(spans2[j2]),)
    #             if h_span_pair2is_valid[span_pair]:
    #                 yield (j1, j2)
    #
    #     if len(spans_list) == 2:
    #         return list(spans_pair2j_pairs_deliminated(spans_list))
    #
    #     def j_tuple_iter():
    #         j_pairs_head = list(spans_pair2j_pairs_deliminated(spans_list[:2]))
    #         j_tuples_tail = list(spans_pair2j_pairs_deliminated(spans_list[1:]))
    #
    #         h_j1_to_l = h_gb_tree(j_tuples_tail, [ig(0)])
    #
    #         for j_pair in j_pairs_head:
    #             l_tail = h_j1_to_l.get(j_pair[1], [])
    #             for j_tuple in l_tail:
    #                 yield tchain(j_pair[:1], j_tuple)
    #
    #     return list(j_tuple_iter())

    @classmethod
    def str_span_pattern2match_full(cls, str_in, span, pattern):
        from foxylib.tools.regex.regex_tool import RegexTool
        str_sub = cls.str_span2str(str_in, span)
        if str_sub is None:
            return None

        m = RegexTool.pattern_str2match_full(pattern, str_sub)
        return m

    @classmethod
    def str_span2is_blank_or_nullstr(cls, str_in, span):
        from foxylib.tools.regex.regex_tool import RegexTool
        return cls.str_span_pattern2match_full(str_in, span, RegexTool.pattern_blank_or_nullstr())



    @classmethod
    @VersionTool.deprecated(reason="Use SpanTool.spans_list_f_gap2j_tuples_valid instead. Function is still functioning")
    def _str_spans_list2j_tuples_delimited(cls, str_in, spans_list, p_delim):
        from foxylib.tools.span.span_tool import SpanTool


        def span_gap2valid(span):
            m = cls.str_span_pattern2match_full(str_in, span, p_delim)
            return m is not None


        return SpanTool.spans_list_f_gap2j_tuples_valid(spans_list, span_gap2valid)


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
    def str_span2str(cls, str_in, span):
        if str_in is None: return None
        if span is None: return None

        if span[0]>span[1]:
            return None

        str_out = str_in[span[0]:span[1]]
        return str_out

    @classmethod
    def str2split(cls, s, *args,**kwargs):
        logger = FoxylibLogger.func2logger(cls.str2split)
        if s is None: return s

        # logger.debug({"s":s, "args":args, "kwargs":kwargs,})
        return s.split(*args,**kwargs)

    @classmethod
    def str2splitlines(cls, s, *_, **__):
        logger = FoxylibLogger.func2logger(cls.str2split)
        if s is None: return s

        # logger.debug({"s":s, "args":args, "kwargs":kwargs,})
        return s.splitlines(*_, **__)

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


    # @classmethod
    # def str_terms2h_term2span(cls, str_in, terms):
    #     h = {}
    #     for term in terms:
    #         index = str_in.find(term)
    #         if index < 0: continue
    #
    #         h[term] = (index,index+len(term))
    #     return h




    # @classmethod
    # def str_queries2span_list(cls, str_in, query_set,):
    #     from foxylib.tools.regex.regex_tool import RegexTool
    #     rstr = RegexTool.rstr_list2or(query_set)
    #     p = re.compile(rstr, re.I)


format_str = StringTool.format_str


str2strip = StringTool.str2strip
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