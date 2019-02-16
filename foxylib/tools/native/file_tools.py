import codecs

from foxylib.native.str_tools import str2strip


class FileToolkit:
    def filepath2utf8(filepath,
                      encoding=None,
                      f_open=None,
                      ):
        if f_open is None:
            if encoding is None: encoding = "utf-8"
            f_open = lambda x: codecs.open(x, "rb", encoding=encoding)

        with f_open(filepath) as f:
            s_dec = f.read()

        return s_dec

    def filepath2utf8_lines(filepath,
                      encoding=None,
                      f_open=None,
                      ):
        if f_open is None:
            if encoding is None: encoding = "utf-8"
            f_open = lambda x: codecs.open(x, "rb", encoding=encoding)

        with f_open(filepath) as f:
            for s in f:
                yield str2strip(s)

filepath2utf8 = FileToolkit.filepath2utf8

