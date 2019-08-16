import ast
import re

from foxylib.tools.log.logger_tools import FoxylibLogger


def str2strip(s): return s.strip() if s else s
def str2rstrip(s): return s.rstrip() if s else s
def str2splitlines(s): return s.splitlines() if s else s
def str2lower(s): return s.lower() if s else s
def join_str(s, *args, **kwargs): return s.join(*args, **kwargs) if s else s




class StringToolkit:
    @classmethod
    def format_str(cls, s, *args, **kwargs):
        logger = FoxylibLogger.func2logger(cls.format_str)
        if not s: return s

        # logger.debug({"s":s,"args":args, "kwargs":kwargs})
        return s.format(*args, **kwargs)

    @classmethod
    def quoted2stripped(cls, s_IN, ):
        try:
            MODULE = ast.parse(s_IN)
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
    def str_se2str(cls, *_, **__):
        return cls.str_span2str(*_, **__)

    @classmethod
    def str_span2str(cls, str_in, se):
        if str_in is None: return None
        if se is None: return None

        str_out = str_in[se[0]:se[1]]
        if not str_out: return None

        return str_out

    @classmethod
    def str2split(cls, s, *args,**kwargs):
        logger = FoxylibLogger.func2logger(cls.str2split)
        if not s: return s

        # logger.debug({"s":s, "args":args, "kwargs":kwargs,})
        return s.split(*args,**kwargs)

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


format_str = StringToolkit.format_str

str2split = StringToolkit.str2split
escape_quotes = StringToolkit.escape_quotes
escape_doublequotes = StringToolkit.escape_doublequotes
whitespace2stripped = StringToolkit.whitespace2stripped
str2has_nw = StringToolkit.str2has_none_whitespace
str2is_pound_comment = StringToolkit.str2is_pound_comment
is_string = StringToolkit.is_string
str_format2escaped = StringToolkit.str_format2escaped