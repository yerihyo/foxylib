from functools import lru_cache

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.jinja2.jinja2_tool import Jinja2Renderer


class FoxylibJinja2:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=256))
    def filepath2utf8(cls, textfile):
        return FileTool.filepath2utf8(textfile)

    @classmethod
    def textfile2text(cls, textfile, data=None, env=None):
        text = cls.filepath2utf8(textfile)
        if text is None:
            return None

        return Jinja2Renderer.text2text(text, data=data, env=env)
