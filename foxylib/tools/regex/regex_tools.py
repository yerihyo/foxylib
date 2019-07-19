from abc import ABC, abstractmethod

import re
from functools import lru_cache

from future.utils import lmap, lfilter
from nose.tools import assert_true

from foxylib.tools.collections.collections_tools import l_singleton2obj, lchain
from foxylib.tools.string.string_tools import format_str


class RegexToolkit:
    @classmethod
    def str_list2rstr_or(cls, l):
        return r"|".join(lmap(re.escape, l))

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
    def rstr2parenthesised(cls, s, rstr_pars=None):
        if rstr_pars is None:
            rstr_pars = (r"\(",r"\)")
        return format_str(r"{}{}{}",
                          cls.rstr2wrapped(rstr_pars[0]),
                          cls.rstr2wrapped(s),
                          cls.rstr2wrapped(rstr_pars[1]),
                          )

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

    @classmethod
    def rstr2wrapped(cls, rstr):
        return r"(?:{})".format(rstr)


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
        return list(m.span())

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
    def match_group2str(cls, m, g):
        assert_true(g)
        if not m: return m

        return m.group(g)

    @classmethod
    def match2explode(cls, str_in, m):
        if not m: return str_in

        s,e = MatchToolkit.match2span(m)
        t = (str_in[:s], str_in[s:e], str_in[e:])
        return t

class RegexNodeToolkit:
    class Node(ABC):
        @classmethod
        @abstractmethod
        def name(cls): pass

        @classmethod
        @abstractmethod
        def rstr_format(cls, *_, **__): pass

        @classmethod
        @abstractmethod
        def subnode_list(cls): pass

    @classmethod
    def rstr2node(cls, rstr):
        class AnonymousNode(RegexNodeToolkit.Node):
            @classmethod
            def name(cls): return None

            @classmethod
            def rstr_format(cls): return lambda: rstr

            @classmethod
            def subnode_list(cls): return None
        return AnonymousNode

    @classmethod
    def tuple2node(cls, t):
        name, f_rstr_format, subnode_list = t

        class NamedNode(RegexNodeToolkit.Node):
            @classmethod
            def name(cls): return name

            @classmethod
            def rstr_format(cls,*_,**__): return f_rstr_format(*_,**__)

            @classmethod
            def subnode_list(cls): return subnode_list

        return NamedNode

    # @classmethod
    # def rstr2node(cls, t):
    #     name, rstr_format, subnode_list = t
    #     def f(*_,**__): return rstr_format
    #     return cls.tuple2node([name,f,subnode_list])


    @classmethod
    def node_list2groupname(cls, node_list):
        name_list = lmap(lambda x: x.name(), node_list)
        return "__".join(name_list)

    @classmethod
    def _node_parents2name(cls, node, ancestors=None,):
        l = lchain(ancestors or [], [node])
        return cls.node_list2groupname(l)

    @classmethod
    def _h_node2args_kwargs(cls, h, node):
        if not h: return [], {}

        args_kwargs = h.get(node)
        if not args_kwargs: return [], {}

        return args_kwargs

    @classmethod
    def _node2rstr_unnamed(cls, node, ancestors=None, h_node2signature=None,):
        subnode_list = node.subnode_list()

        ancestors_and_me = lchain(ancestors or [],[cls])
        rstr_list_subnode = [cls.node2rstr(sn, ancestors_and_me, named=True,) for sn in subnode_list]

        args, kwargs = cls._h_node2args_kwargs(h_node2signature, node)
        rstr = format_str(node.rstr_format(*args, **kwargs), *rstr_list_subnode)
        return rstr

    @classmethod
    def node2rstr(cls, node, ancestors=None, named=False, h_node2signature=None,):
        rstr_unnamed = cls._node2rstr_unnamed(node, ancestors=ancestors, h_node2signature=h_node2signature)
        if not named:
            return RegexToolkit.rstr2wrapped(rstr_unnamed)

        rstr_named = format_str(r"(?P<{}>{})",
                                cls._node_parents2name(node, ancestors=ancestors),
                                rstr_unnamed,
                                )
        return rstr_named

