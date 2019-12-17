import ast
import re

from future.utils import lmap, lfilter

from foxylib.tools.collections.collections_tool import IterTool
from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.span.span_tools import SpanToolkit


class StringToolkit:
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

        str_out = str_in[span[0]:span[1]]
        if not str_out: return None

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
        from foxylib.tools.span.span_tools import SpanToolkit
        str_out = SpanToolkit.list_spans_func2processed(str_in, span_list, func, f_list2chain="".join)
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

    @classmethod
    def str_format2escaped(cls, s_format):
        return re.sub("\{[\w,]+\}","{\g<0>}",s_format)

    @classmethod
    def dict2f_sub(cls, h):
        # Create a regular expression from all of the dictionary keys
        from foxylib.tools.regex.regex_tools import RegexToolkit
        rstr = RegexToolkit.join(r"|".join(map(re.escape, h.keys())))
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
    #     from foxylib.tools.regex.regex_tools import RegexToolkit
    #     rstr = RegexToolkit.rstr_list2or(query_set)
    #     p = re.compile(rstr, re.I)


format_str = StringToolkit.format_str


str2strip = StringToolkit.str2strip
str2rstrip = StringToolkit.str2rstrip
str2lower = StringToolkit.str2lower
str2upper = StringToolkit.str2upper
join_str = StringToolkit.join_str

str2split = StringToolkit.str2split
str2splitlines = StringToolkit.str2splitlines
escape_quotes = StringToolkit.escape_quotes
escape_doublequotes = StringToolkit.escape_doublequotes
whitespace2stripped = StringToolkit.whitespace2stripped
str2has_nw = StringToolkit.str2has_none_whitespace
str2is_pound_comment = StringToolkit.str2is_pound_comment
is_string = StringToolkit.is_string
str_format2escaped = StringToolkit.str_format2escaped