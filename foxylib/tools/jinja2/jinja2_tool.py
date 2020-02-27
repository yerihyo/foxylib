import logging
from functools import lru_cache

from jinja2 import Template, Environment, Undefined
from markupsafe import Markup
from nose.tools import assert_true

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


# https://stackoverflow.com/questions/6190348/jinja2-ignore-undefinederrors-for-objects-that-arent-found
# class SilentUndefined(Undefined):
#     '''
#     Dont break pageloads because vars arent there!
#     '''
#     def _fail_with_undefined_error(self, *args, **kwargs):
#         logging.exception('JINJA2: something was undefined!')
#         return None

# https://stackoverflow.com/questions/6182498/jinja2-how-to-make-it-fail-silently-like-djangotemplate/6192308
class SilentUndefined(Undefined):
    __unicode__ = lambda *_, **__: u""
    __str__ = lambda *_, **__: u""
    __call__ = lambda *_, **__: SilentUndefined()
    __getattr__ = lambda *_, **__: SilentUndefined()

class Jinja2Tool:
    @classmethod
    def env_silent(cls):
        return Environment(autoescape=True, undefined=SilentUndefined)

    @classmethod
    @lru_cache(maxsize=2)
    def _js_escapes(cls):
        h = {
            '\\': '\\u005C',
            '\'': '\\u0027',
            '"': '\\u0022',
            '>': '\\u003E',
            '<': '\\u003C',
            '&': '\\u0026',
            '=': '\\u003D',
            '-': '\\u002D',
            ';': '\\u003B',
            u'\u2028': '\\u2028',
            u'\u2029': '\\u2029'
        }
        # Escape every ASCII character with a value less than 32.
        h.update(('%c' % z, '\\u%04X' % z) for z in range(32))
        return h

    @classmethod
    def escape_js(cls, value):
        if value is None:
            return None

        if not isinstance(value, str):
            return value

        return value.replace('"', r'\"')

    @classmethod
    def data2js_escaped(cls, data):
        return {k:cls.escape_js(v) for k,v in data.items()}

    @classmethod
    def tmplt_str2str(cls, str_tmplt, data=None, env=None):
        # if autoescape is None:
        #     autoescape = False

        if data is None:
            data = {}

        if env is None:
            template = Template(str_tmplt,)
        else:
            template = env.from_string(str_tmplt)

        # data_escaped = cls.data2js_escaped(data)
        return template.render(**data)

    @classmethod
    def html2marked(cls, html): return Markup(html)

    @classmethod
    def tmplt_str2html(cls, html_tmplt, data=None, env=None):
        if env is None:
            env = Environment(autoescape=True)

        assert_true(env.autoescape)

        s = cls.tmplt_str2str(html_tmplt, data=data, env=env)
        return Markup(s)

    @classmethod
    def tmplt_file2str(cls, filepath, data=None, env=None):
        logger = FoxylibLogger.func_level2logger(cls.tmplt_file2str, logging.DEBUG)
        str_tmplt = FileTool.filepath2utf8(filepath)
        # logger.debug({"filepath":filepath,"str_tmplt": str_tmplt})
        return cls.tmplt_str2str(str_tmplt, data=data, env=env)

    @classmethod
    def tmplt_file2html(cls, filepath, data=None, env=None):
        str_tmplt = FileTool.filepath2utf8(filepath)
        return cls.tmplt_str2html(str_tmplt, data=data, env=env)






tmplt_str2str = Jinja2Tool.tmplt_str2str
tmplt_file2str = Jinja2Tool.tmplt_file2str