from future.utils import lmap
from jinja2 import Template, Undefined, escape, Environment
from markupsafe import Markup

from foxylib.tools.collections.collections_tool import smap, tmap
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

    @classmethod
    def env(cls):
        return Environment(undefined=cls)

class Jinja2Tool_Deprecated:
    pass
    # @classmethod
    # @lru_cache(maxsize=1)
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
    def _json2escaped(cls, j):
        if not j:
            return j

        if isinstance(j, (list,)):
            return lmap(cls._json2escaped, j)

        if isinstance(j, (tuple,)):
            return tmap(cls._json2escaped, j)

        if isinstance(j, (set,)):
            return smap(cls._json2escaped, j)

        if isinstance(j, (dict,)):
            return {k: cls._json2escaped(v)
                    for k, v in j.items()}

        if isinstance(j, (str,)):
            return escape(j)

        return j

    @classmethod
    def env_text2template(cls, env, template_text):
        if env:
            # Environment.from_string
            return env.from_string(template_text)
        return Template(template_text)

    @classmethod
    def env_markup2template(cls, env, template_markup):
        return cls.env_text2template(env, escape(template_markup))

    @classmethod
    def template2text(cls, template, data=None,):
        return template.render(**data)

    @classmethod
    def template2markup(cls, template, data=None,):
        text = template.render(**(cls._json2escaped(data) or {}))
        return Markup(text)

    @classmethod
    def text2text(cls, template_text, data=None, env=None):
        if not template_text:
            return None
        
        template = cls.env_text2template(env, template_text)
        return cls.template2text(template, data=data)

    @classmethod
    def markup2markup(cls, template_markup, data=None, env=None):
        template = cls.env_markup2template(env, template_markup)
        return cls.template2markup(template, data=data)

    @classmethod
    def textfile2text(cls, textfile, data=None, env=None):
        text = FileTool.filepath2utf8(textfile)
        if text is None:
            return None

        return cls.text2text(text, data=data, env=env)

    @classmethod
    def htmlfile2markup(cls, htmlfile, data=None, env=None):
        text = FileTool.filepath2utf8(htmlfile)
        return cls.markup2markup(Markup(text), data=data, env=env)


