import re
from functools import lru_cache

from future.utils import lmap, lfilter
from nose.tools import assert_true

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.collections.collections_tool import l_singleton2obj, lchain
from foxylib.tools.native.class_tool import cls2name
from foxylib.tools.span.span_tool import SpanTool, list_span2sublist
from foxylib.tools.string.string_tool import format_str


class RegexTool:
    @classmethod
    def rstr_email(cls):
        # https://emailregex.com/
        return r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    @classmethod
    def rstr_list2or(cls, l_in):
        l_sorted = sorted(l_in, key=lambda x: -len(x))
        rstr_or = r"|".join(lmap(cls.rstr2wrapped, l_sorted))
        return rstr_or

    @classmethod
    def rstr2rstr_words_prefixed(cls, rstr, rstr_prefix_list=None, ):
        # \b (word boundary)_does not work when str_query quoted or double-quoted
        # might wanna use string matching than regex because of speed issue
        if not rstr_prefix_list: rstr_prefix_list = [""]

        l = [format_str(r"(?<=^{0})|(?<=\s{0})|(?<=\b{0})", rstr_prefix)
             for rstr_prefix in rstr_prefix_list]
        rstr_pre = cls.join(r"|", l)

        return format_str(r'{0}{1}',
                          cls.rstr2wrapped(rstr_pre),
                          cls.rstr2wrapped(rstr),
                          )

    @classmethod
    def rstr2rstr_words_suffixed(cls, rstr, rstr_suffix=None, ):
        # \b (word boundary)_does not work when str_query quoted or double-quoted
        # might wanna use string matching than regex because of speed issue
        rstr_suf = r"(?=(?:{0})(?:\s|\b|$))".format(rstr_suffix or "")
        return r'(?:{0}){1}'.format(rstr, rstr_suf)

    @classmethod
    def rstr2rstr_words(cls, rstr, rstr_prefix_list=None, rstr_suffix=None, ):
        # \b (word boundary)_does not work when str_query quoted or double-quoted
        # might wanna use string matching than regex because of speed issue

        rstr_prefixed = cls.rstr2rstr_words_prefixed(rstr, rstr_prefix_list=rstr_prefix_list)
        rstr_words = cls.rstr2rstr_words_suffixed(rstr_prefixed, rstr_suffix=rstr_suffix)
        return rstr_words

    @classmethod
    def rstr2rstr_eos(cls, rstr, ):
        return r"^{}$".format(rstr)

    @classmethod
    def rstr2parenthesised(cls, s, rstr_pars=None):
        if rstr_pars is None:
            rstr_pars = (r"\(", r"\)")
        return format_str(r"{}{}{}",
                          cls.rstr2wrapped(rstr_pars[0]),
                          cls.rstr2wrapped(s),
                          cls.rstr2wrapped(rstr_pars[1]),
                          )

    @classmethod
    def rstr2rstr_line_prefixed(cls, rstr, rstr_prefix=None, ):
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
    def name_rstr2named(cls, name, rstr):
        return format_str(r"(?P<{0}>{1})", name, rstr)

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_blank(cls):
        return re.compile(r"\s+")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_blank_or_nullstr(cls):
        return re.compile(r"\s*")

    @classmethod
    def p_str2m_uniq(cls, pattern, s):
        m_list = list(pattern.finditer(s))
        if not m_list: return None

        m = l_singleton2obj(m_list)
        return m

    # @classmethod
    # def rstr2rstr_last(cls, rstr):
    #     return r"(?:{})(?!.*(?:{}))".format(rstr)

    @classmethod
    def rstr2wrapped(cls, rstr):
        return r"(?:{})".format(rstr)


    @classmethod
    def pattern_str2match_full(cls, p, str_in):
        m = p.match(str_in)
        if not m:
            return m

        if not m.end() == len(str_in):
            return None

        return m


class MatchTool:
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
        return cls.match2span(m)

    @classmethod
    def match2span(cls, m):
        return list(m.span())

    @classmethod
    def match_group2span(cls, m, groupname):
        return list(m.span(groupname))

    @classmethod
    def match2len(cls, m):
        return SpanTool.span2len(cls.match2span(m))

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
    def match2str_group_list(cls, m):
        return [name for name, value in m.groupdict().items() if value is not None]

    @classmethod
    def match2str_group(cls, m):
        l = cls.match2str_group_list(m)
        return l_singleton2obj(l)

    @classmethod
    def match_group2str(cls, m, g):
        assert_true(g)
        if not m: return m

        return m.group(g)

    @classmethod
    def match2explode(cls, str_in, m):
        if not m: return str_in

        s, e = MatchTool.match2span(m)
        t = (str_in[:s], str_in[s:e], str_in[e:])
        return t

    @classmethod
    def match_list_limit2span_best(cls, m_list, len_limit, f_matches2score,):
        if not m_list:
            return None


        span_list_document = lmap(match2span, m_list)
        span_list_match = list(SpanTool.span_list_limit2span_of_span_longest_iter(span_list_document, len_limit))
        if not span_list_match:
            return None

        # text_list = lmap(match2text, m_list)
        span_best_match = max(span_list_match,
                              key=lambda span_m: f_matches2score(list_span2sublist(m_list, span_m)))
        span_best_document = SpanTool.span_list_span2span_big(span_list_document, span_best_match)
        return span_best_document


class RegexNodeTool:
    # @classmethod
    # def node2name(cls, node): return node.h["name"]
    # @classmethod
    # def node2repr(cls, node):
    #     return "{0}({1})".format(cls2name(obj2cls(node)), cls.node2name(node))

    class Type:
        FORMAT_NODE = "format_node"
        RSTR_NODE = "rstr_node"

    # class FormatNode:
    #     def __init__(self, name, func, subnode_list):
    #         self.h = {"name": name, "func": func, "subnode_list": subnode_list, }
    #
    #     def __repr__(self):
    #         return RegexNodeTool.node2repr(self)
    #
    #
    #     def subnode_list(self): return self.h["subnode_list"]
    #
    #     def rstr_format(self, *_, **__):
    #         return self.h["func"](*_, **__)
    #
    #     @classmethod
    #     def create(cls, *_, **__): return cls(*_, **__)
    #
    # class RstrNode:
    #     def __init__(self, name, func, ):
    #         self.h = {"name": name, "func": func, }
    #
    #     def __repr__(self):
    #         return RegexNodeTool.node2repr(self)
    #
    #     def rstr(self, *_, **__):
    #         return self.h["func"](*_, **__)
    #
    #     @classmethod
    #     def create(cls, *_, **__): return cls(*_, **__)

    @classmethod
    def node_list2groupname(cls, node_list):
        logger = FoxylibLogger.func2logger(cls.node_list2groupname)
        # logger.debug({"node_list": node_list})
        name_list = lmap(cls2name, node_list)
        return "__".join(name_list)

    @classmethod
    def _node_parents2name(cls, node, ancestors, ):
        l = lchain(ancestors, [node])
        return cls.node_list2groupname(l)

    @classmethod
    def _h_node2args_kwargs(cls, h, node):
        if not h: return [], {}
        logger = FoxylibLogger.func2logger(cls._h_node2args_kwargs)

        args_kwargs = h.get(node)
        # logger.debug({"h": h, "node": node, "args_kwargs":args_kwargs})
        if not args_kwargs: return [], {}

        return args_kwargs

    @classmethod
    def node2type(cls, node): return node.type()

    @classmethod
    def _node2rstr_unnamed(cls, node, ancestors, args=None, kwargs=None,):
        logger = FoxylibLogger.func2logger(cls._node2rstr_unnamed)
        _args = args or []
        _kwargs = kwargs or {}
        # logger.debug({"node": node, "args": args, "kwargs": kwargs, "type":cls.node2type(node),
        #               "h_node2ak": h_node2ak,
        #               })
        if cls.node2type(node) == cls.Type.RSTR_NODE:
            rstr = node.rstr(*_args, **_kwargs)
            return rstr

        subnode_list = node.subnode_list()
        ancestors_and_me = lchain(ancestors, [node])
        rstr_list_subnode = [cls._node2rstr_named(sn, ancestors_and_me, args=args, kwargs=kwargs) for sn in subnode_list]

        str_format = node.rformat(*_args, **_kwargs)
        rstr = format_str(str_format, *rstr_list_subnode)
        return rstr

    @classmethod
    def _node2rstr_named(cls, node, ancestors, args=None, kwargs=None):
        logger = FoxylibLogger.func2logger(cls._node2rstr_named)
        # logger.debug({"node":node, "ancestors": ancestors, })
        rstr_unnamed = cls._node2rstr_unnamed(node, ancestors, args=args, kwargs=kwargs)
        rstr_named = RegexTool.name_rstr2named(cls._node_parents2name(node, ancestors), rstr_unnamed)
        return rstr_named

    @classmethod
    def node2rstr(cls, node, named=True, args=None, kwargs=None,):
        logger = FoxylibLogger.func2logger(cls.node2rstr)
        # logger.debug({"node":node, "ancestors": ancestors, })
        if named:
            return cls._node2rstr_named(node, [], args=args, kwargs=kwargs)
        else:
            return cls._node2rstr_unnamed(node, [], args=args, kwargs=kwargs)

    @classmethod
    def node2pattern(cls, node, *_, **__):
        rstr = cls.node2rstr(node, *_, **__)
        return re.compile(rstr)


    @classmethod
    def match_nodes2groupname_list(cls, m, cls_node_list):
        str_group_list = MatchTool.match2str_group_list(m)

        nodename_list = lmap(cls2name, cls_node_list)
        str_group_list_related = lfilter(lambda s:s.split("__")[-1] in nodename_list, str_group_list)
        return str_group_list_related


rstr2wrapped = RegexTool.rstr2wrapped
p_blank_or_nullstr = RegexTool.pattern_blank_or_nullstr

match2start = MatchTool.match2start
match2end = MatchTool.match2end
match2span = MatchTool.match2span
match2text = MatchTool.match2text

# FormatNode = RegexNodeTool.FormatNode
# RstrNode = RegexNodeTool.RstrNode
