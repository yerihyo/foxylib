import jinja2
from future.utils import lmap
from markupsafe import Markup

from foxylib.tools.flowcontrol.condition_tools import ternary
from foxylib.tools.string.string_tools import escape_doublequotes


class HTMLToolkit:
    @classmethod
    def conditional_escape(cls, s):
        return jinja2.escape(s)

    @classmethod
    def format_html(cls, s_tmplt, *args, **kwargs):
        m = Markup(s_tmplt)
        return m.format(*args, **kwargs)

    @classmethod
    def join_html(cls, delim, l):
        delim_safe = cls.conditional_escape(delim)
        html = delim_safe.join(lmap(cls.conditional_escape, l))
        return Markup(html)

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

mark_safe = Markup
join_html = HTMLToolkit.join_html
format_html = HTMLToolkit.format_html
wrap_html_tag = HTMLToolkit.wrap_html_tag
html_tag_singleton = HTMLToolkit.html_tag_singleton
conditional_escape = HTMLToolkit.conditional_escape
