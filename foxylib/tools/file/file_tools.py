import codecs
import os

from past.builtins import reduce

from foxylib.tools.string.string_tools import str2strip


class FileToolkit:
    @classmethod
    def filepath2utf8(cls,
                      filepath,
                      encoding=None,
                      f_open=None,
                      ):
        if f_open is None:
            if encoding is None: encoding = "utf-8"
            f_open = lambda x: codecs.open(x, "rb", encoding=encoding)

        with f_open(filepath) as f:
            s_dec = f.read()

        return s_dec

    @classmethod
    def filepath2utf8_lines(cls,
                            filepath,
                      encoding=None,
                      f_open=None,
                      ):
        if f_open is None:
            if encoding is None: encoding = "utf-8"
            f_open = lambda x: codecs.open(x, "rb", encoding=encoding)

        with f_open(filepath) as f:
            for s in f:
                yield str2strip(s)

    @classmethod
    def dirname(cls, filepath, count=1):
        return reduce(lambda x,f:f(x), [os.path.dirname]*count, filepath)

class DirToolkit:
    @classmethod
    def makedirs_if_empty(cls, dirpath):
        if not os.path.exists(dirpath): os.makedirs(dirpath)

filepath2utf8 = FileToolkit.filepath2utf8
makedirs_if_empty = DirToolkit.makedirs_if_empty

