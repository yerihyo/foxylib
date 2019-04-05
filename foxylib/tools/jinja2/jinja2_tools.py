import os
from functools import lru_cache

from jinja2 import Environment, BaseLoader, FileSystemLoader, Template

from foxylib.tools.file.file_tools import FileToolkit


class Jinja2Toolkit:
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
    def tmplt_str2str(cls, str_tmplt, data, autoescape=False):
        template = Template(str_tmplt, autoescape=autoescape)
        data_escaped = cls.data2js_escaped(data)
        return template.render(**data_escaped)

    @classmethod
    def tmplt_file2str(cls, filepath, data):
        str_tmplt = FileToolkit.filepath2utf8(filepath)
        return cls.tmplt_str2str(str_tmplt, data)


tmplt_str2str = Jinja2Toolkit.tmplt_str2str
tmplt_file2str = Jinja2Toolkit.tmplt_file2str