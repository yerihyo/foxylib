from jinja2 import Template, Undefined, escape
from markupsafe import Markup

from foxylib.tools.file.file_tool import FileTool
# https://stackoverflow.com/questions/6182498/jinja2-how-to-make-it-fail-silently-like-djangotemplate/6192308
from foxylib.tools.native.native_tool import equal_type_and_value


# https://stackoverflow.com/questions/6190348/jinja2-ignore-undefinederrors-for-objects-that-arent-found
# class SilentUndefined(Undefined):
#     '''
#     Dont break pageloads because vars arent there!
#     '''
#     def _fail_with_undefined_error(self, *args, **kwargs):
#         logging.exception('JINJA2: something was undefined!')
#         return None


class SilentUndefined(Undefined):
    __unicode__ = lambda *_, **__: u""
    __str__ = lambda *_, **__: u""
    __call__ = lambda *_, **__: SilentUndefined()
    __getattr__ = lambda *_, **__: SilentUndefined()

class Jinja2Tool_Deprecated:
    pass
    # @classmethod
    # @lru_cache(maxsize=2)
    # def _js_escapes(cls):
    #     h = {
    #         '\\': '\\u005C',
    #         '\'': '\\u0027',
    #         '"': '\\u0022',
    #         '>': '\\u003E',
    #         '<': '\\u003C',
    #         '&': '\\u0026',
    #         '=': '\\u003D',
    #         '-': '\\u002D',
    #         ';': '\\u003B',
    #         u'\u2028': '\\u2028',
    #         u'\u2029': '\\u2029'
    #     }
    #     # Escape every ASCII character with a value less than 32.
    #     h.update(('%c' % z, '\\u%04X' % z) for z in range(32))
    #     return h

class Jinja2Tool:
    @classmethod
    def equal(cls, result_01, result_02):
        return equal_type_and_value(result_01, result_02)

class Jinja2Renderer:
    @classmethod
    def _data2escaped(cls, data):
        if not data:
            return data

        return {k:escape(v) for k,v in data.items()}

    @classmethod
    def text2text(cls, template_text, data=None):
        template = Template(template_text)
        return template.render(**data)

    @classmethod
    def markup2markup(cls, template_markup, data=None):
        template = Template(escape(template_markup))
        return Markup(template.render(**cls._data2escaped(data)))

    @classmethod
    def textfile2text(cls, textfile, data=None):
        text = FileTool.filepath2utf8(textfile)
        return cls.text2text(text, data=data)

    @classmethod
    def htmlfile2markup(cls, htmlfile, data=None):
        text = FileTool.filepath2utf8(htmlfile)
        return cls.markup2markup(Markup(text), data=data)


