import jinja2
from bs4 import BeautifulSoup
from future.utils import lmap, lfilter
from markupsafe import Markup
from nose.tools import assert_not_in

from foxylib.tools.collections.collections_tools import merge_dicts, DictToolkit, zip_strict, lzip_strict
from foxylib.tools.flowcontrol.condition_tools import ternary
from foxylib.tools.string.string_tools import escape_doublequotes


class HTMLToolkit:
    @classmethod
    def escape(cls, s):
        return jinja2.escape(s)

    @classmethod
    def str2html_comment(cls, s):
        return Markup("<!-- {0} -->".format(cls.escape(s)))

    @classmethod
    def head_plist2html(cls, headpair_list):

        html_css_list, html_js_list = lzip_strict(*headpair_list)

        html_css = join_html("\n", lfilter(bool,html_css_list))
        html_js = join_html("\n", lfilter(bool,html_js_list))

        l = [HTMLToolkit.str2html_comment("CSS import"),
             html_css,
             "",
             HTMLToolkit.str2html_comment("JS import"),
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
        delim_safe = cls.escape(delim)
        html = delim_safe.join(lmap(cls.escape, l))
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
    def vwrite_attrs(cls, h, k, v_in):
        if k in ["class","style"]:
            h[k] = " ".join([h.get(k, ""), v_in])
            return h
        else:
            return DictToolkit.VWrite.overwrite(h, k, v_in)

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
        soup = BeautifulSoup(s)
        return soup.get_text()

mark_safe = Markup
join_html = HTMLToolkit.join_html
join_html_and_wrap = HTMLToolkit.join_html_and_wrap
format_html = HTMLToolkit.format_html
wrap_html_tag = HTMLToolkit.wrap_html_tag
html_tag_singleton = HTMLToolkit.html_tag_singleton
# conditional_escape = HTMLToolkit.conditional_escape
escape = HTMLToolkit.escape


html_div_height = HTMLToolkit.html_div_height
html_div_height_nl = HTMLToolkit.html_div_height_nl

url2html = HTMLToolkit.url2html
