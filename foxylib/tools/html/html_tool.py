import logging

import jinja2
from bs4 import BeautifulSoup
from future.utils import lmap, lfilter
from markupsafe import Markup
from nose.tools import assert_not_in

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.collections.collections_tool import merge_dicts, DictTool, lzip_strict
from foxylib.tools.flowcontrol.flowcontrol_tool import ternary
from foxylib.tools.string.string_tool import escape_doublequotes


class HTMLTool:
    @classmethod
    def escape(cls, s):
        return jinja2.escape(s)

    @classmethod
    def str2html_comment(cls, s):
        return Markup("<!-- {0} -->".format(cls.escape(s)))

    @classmethod
    def html_meta_viewport(cls):
        return Markup('<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    @classmethod
    def head_plist2html(cls, headpair_list):

        html_css_list, html_js_list = lzip_strict(*headpair_list)

        html_css = join_html("\n", lfilter(bool,html_css_list))
        html_js = join_html("\n", lfilter(bool,html_js_list))

        l = [HTMLTool.str2html_comment("CSS import"),
             html_css,
             "",
             HTMLTool.str2html_comment("JS import"),
             html_js,
             ]
        html = join_html("\n",l)
        return html

    # @classmethod
    # def conditional_escape(cls, s):
    #     return cls.escape(s)

    @classmethod
    def format_html(cls, s_tmplt, *args, **kwargs):
        m = Markup(s_tmplt)
        return m.format(*args, **kwargs)

    @classmethod
    def join_html(cls, delim, l):
        logger = FoxylibLogger.func_level2logger(cls.join_html, logging.DEBUG)
        # delim_safe = cls.escape(delim)
        # html_delim = Markup(delim)
        # logger.debug({"delim":delim,
        #               "l":l,
        #               })
        html = cls.escape(delim).join(lmap(cls.escape, l))
        return Markup(html)

    @classmethod
    def join_html_and_wrap(cls, l, tag, attrs=None, delim=""):
        html = wrap_html_tag(join_html("\n", l),
                             tag,
                             attrs=attrs,
                             delim=delim,
                             )
        return html

    @classmethod
    def kv_iter2html_attrs(cls, iterable):
        return cls.join_html(" ",
                         [ternary(v is None,
                                  f_true=lambda b: k,
                                  f_false=lambda b: cls.format_html("{0}=\"{1}\"",
                                                                k,
                                                                escape_doublequotes(str(v)),
                                                                ),
                                  )
                          #                       if v is not None else k
                          for k, v in iterable])

    @classmethod
    def html_tag_singleton(cls, tag, attrs=None):
        html_attrs = cls.kv_iter2html_attrs(attrs.items()) if attrs else ""
        return cls.format_html("<{0} {1} />", tag, html_attrs)

    @classmethod
    def wrap_html_tag(cls, s, tag, attrs=None, delim=""):
        html_attrs = cls.kv_iter2html_attrs(attrs.items()) if attrs else ""

        l = [cls.format_html("<{0} {1}>", tag, html_attrs),
             s,
             cls.format_html("</{0}>", tag),
             ]
        return cls.join_html(delim, l)

    @classmethod
    def match_list2sub(cls, s_in, match_list, s_repl):
        n = len(match_list)

        html_repl = cls.escape(s_repl)

        l = []
        for i,m in enumerate(match_list):


            b1, e1 = m.start(), m.end()
            e0 = match_list[i-1].end() if i>0 else 0

            l.append(cls.escape(s_in[e0:b1]))
            l.append(html_repl)

        e = match_list[-1].end() if match_list else 0
        if e < len(s_in):
            l.append(cls.escape(s_in[e:]))

        return cls.join_html("",l)

    @classmethod
    def match_list_func2subbed(cls, s_in, match_list, f_repl):
        n = len(match_list)

        # html_repl = cls.escape(s_repl)

        l = []
        for i, m in enumerate(match_list):
            b1, e1 = m.start(), m.end()
            e0 = match_list[i - 1].end() if i > 0 else 0

            l.append(cls.escape(s_in[e0:b1]))
            html_repl = f_repl(m)
            l.append(html_repl)

        e = match_list[-1].end() if match_list else 0
        if e < len(s_in):
            l.append(cls.escape(s_in[e:]))

        return cls.join_html("", l)

    @classmethod
    def vwrite_attrs(cls, h, k, v_in):
        if k in ["class","style"]:
            h[k] = " ".join([h.get(k, ""), v_in])
            return h
        else:
            return DictTool.VWrite.overwrite(h, k, v_in)

    @classmethod
    def html_div_height(cls, height, attrs=None):
        a = merge_dicts([attrs,{"style": "height:{0}px;".format(height), },],
                        vwrite=cls.vwrite_attrs)

        html = wrap_html_tag("", "div", attrs=a,)
        return html

    @classmethod
    def html_div_height_nl(cls, height, attrs=None):
        return join_html("", ["\n", cls.html_div_height(height, attrs=attrs), "\n", ])

    # @classmethod
    # def wrap_visible_xs(cls, html):
    #     return wrap_html_tag(html, "div", attrs={"class": "d-sm-none"})
    #
    # @classmethod
    # def wrap_hidden_xs(cls, html):
    #     return wrap_html_tag(html, "div", attrs={"class": "d-none d-sm-block"})


    @classmethod
    def html_div_width(cls, width, attrs={}):
        h_attrs = merge_dicts([attrs,
                               {"style": " ".join(["width:{0}px;".format(width),
                                                   "display:inline-block;",
                                                   ])
                                },
                               ], vwrite=cls.vwrite_attrs)
        html = wrap_html_tag("", "div", attrs=h_attrs)
        return html

    @classmethod
    def html_div_width_nl(cls, width, attrs=None, ):
        return join_html("",
                         ["\n",
                          cls.html_div_width(width, attrs=attrs),
                          "\n",
                          ])


    @classmethod
    def url2html(cls, url, a=None, attrs=None,):
        if a is None:
            a = "↗"
        else:
            assert_not_in("<a", a.split())

        h = merge_dicts([attrs,{"href": url},], vwrite=cls.vwrite_attrs)
        return wrap_html_tag(a, "a", attrs=h)


    @classmethod
    def str2tag_stripped(cls, s):
        if not s: return s

        soup = BeautifulSoup(s)
        return soup.get_text()

    @classmethod
    def nl2br(cls, html_in):
        l_line = html_in.splitlines()
        html = cls.join_html("<br/>",lmap(Markup, l_line))
        return html


class BeautifulsoupTool:
    @classmethod
    def br2nl(cls, soup):
        for br in soup.find_all("br"):
            br.replace_with("\n")
        return soup

    @classmethod
    def node_tag2nl(cls, node, tag):
        for br in node.find_all(tag):
            br.replace_with("\n")
        return node

    @classmethod
    def soup2str(cls, soup):
        return str(soup)

    @classmethod
    def soup2str_notag(cls, soup):
        return soup.get_text()

    @classmethod
    def str2nl_notag(cls, str_in):
        soup = BeautifulSoup(str_in)
        str_out = BeautifulsoupTool.soup2str_notag(BeautifulsoupTool.br2nl(soup))
        return str_out

    @classmethod
    def node2tags_removed(cls, node, tag_list):
        for n in node(tag_list):
            n.extract()  # rip it out
        return node


mark_safe = Markup
join_html = HTMLTool.join_html
join_html_and_wrap = HTMLTool.join_html_and_wrap
format_html = HTMLTool.format_html
wrap_html_tag = HTMLTool.wrap_html_tag
html_tag_singleton = HTMLTool.html_tag_singleton
# conditional_escape = HTMLTool.conditional_escape
escape = HTMLTool.escape


html_div_height = HTMLTool.html_div_height
html_div_height_nl = HTMLTool.html_div_height_nl
nl2br = HTMLTool.nl2br


url2html = HTMLTool.url2html
str2notag = HTMLTool.str2tag_stripped
