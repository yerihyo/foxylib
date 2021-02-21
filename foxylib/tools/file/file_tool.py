import codecs
from pathlib import Path

import logging
import os
from datetime import datetime
from functools import reduce, partial
from mimetypes import guess_type

import pytz
# from magic import from_file

from foxylib.tools.compare.compare_tool import v_pair2is_cmp_satisfied
from foxylib.tools.datetime.pytz_tool import PytzTool

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import str2strip


FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)


class FileTool:

    @classmethod
    def implode(cls, filepath):
        def helper():
            fp = filepath
            while True:
                dirpath, filename = os.path.split(fp)

                if filename:
                    yield filename

                fp = dirpath
                if dirpath == '/':
                    yield ''
                    break

                if not dirpath:
                    break

        return list(reversed(list(helper())))

    @classmethod
    def filepath2mimetype(cls, filepath):
        from foxylib.tools.file.mimetype_tool import MimetypeTool
        return MimetypeTool.url2mimetype(filepath)

    @classmethod
    def filepath2encoding(cls, filepath):
        mimetype, encoding = guess_type(filepath)
        return encoding
        # return from_file(filepath, mime=True)
        # return filetype.guess(filepath)

    @classmethod
    def filepath2bytes(cls,
                      filepath,
                      f_open=None,
                      ):
        if f_open is None:
            f_open = lambda x: open(x, "rb", )

        with f_open(filepath) as f:
            bytes = f.read()

        return bytes

    @classmethod
    def filepath2utf8(cls,
                      filepath,
                      encoding=None,
                      f_open=None,
                      ):
        if f_open is None:
            if encoding is None: encoding = "utf-8"
            f_open = lambda x: codecs.open(x, "rb", encoding=encoding)

        if not os.path.exists(filepath):
            return None

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

        if not os.path.exists(filepath):
            return None

        with f_open(filepath) as f:
            for s in f:
                yield str2strip(s)

    @classmethod
    def filepath2utf8_line_list(cls,*_,**__):
        return list(cls.filepath2utf8_lines(*_,**__))

    @classmethod
    def dirname(cls, filepath, count=1):
        return reduce(lambda x,f:f(x), [os.path.dirname]*count, filepath)

    @classmethod
    def bytes2file(cls, bytes,
                  filepath,
                  f_open=None,
                  ):
        if f_open is None:
            # f_open = lambda filepath: open(filepath, "wb")
            f_open = partial(open, mode="wb")

        OUT_DIR = os.path.dirname(filepath)
        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)

        if os.path.islink(filepath):
            os.unlink(filepath)

        with f_open(filepath) as f:
            f.write(bytes)

    @classmethod
    def encoding2f_codecs_open(cls, encoding, mode):
        def f_open(filepath):
            return codecs.open(filepath, mode=mode, encoding=encoding)

        return f_open

    @classmethod
    def utf82file(cls, utf8, filepath, f_open=None,):
        logger = FoxylibLogger.func_level2logger(cls.utf82file, logging.DEBUG)

        if f_open is None:
            f_open = cls.encoding2f_codecs_open('utf-8', 'w')

        OUT_DIR = os.path.dirname(filepath)
        if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
        if os.path.islink(filepath): os.unlink(filepath)

        with f_open(filepath) as f:
            if utf8:
                print(utf8, file=f)

    @classmethod
    def lines2file(cls, lines, filepath, f_open=None,):

        if f_open is None:
            f_open = cls.encoding2f_codecs_open('utf-8', 'w')

        out_dir = os.path.dirname(filepath)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if os.path.islink(filepath):
            os.unlink(filepath)

        with f_open(filepath) as f:
            for line in lines:
                print(line, file=f)

    @classmethod
    def makedirs_or_skip(cls, dirpath):
        if os.path.exists(dirpath):
            return

        os.makedirs(dirpath)

    @classmethod
    def writeln(cls, fptr, s):
        fptr.write("{}\n".format(s))


    @classmethod
    def filepath2is_empty(cls, filepath):
        return os.stat(filepath).st_size == 0

    # @classmethod
    # def writer2binfilewriter(cls, filepath, writer):
    #     def filewriter(obj, *_, **__):
    #         with open(filepath, 'wb') as f:
    #             writer(obj, f, *_, **__)
    #     return filewriter
    #
    # @classmethod
    # def reader2binfilereader(cls, filepath, reader):
    #     def filereader(*_, **__):
    #         with open(filepath, 'wb') as f:
    #             obj = reader(f, *_, **__)
    #         return obj
    #
    #     return filereader




class FiletimeTool:
    @classmethod
    def dt_always_outdated(cls):
        return None

    @classmethod
    def dt_reject_all(cls):
        return None

    @classmethod
    def dt_allow_if_exists(cls):
        return pytz.utc.localize(datetime.min)

    @classmethod
    def dt2is_uptodate(cls, dt, dt_pivot):
        if dt_pivot == cls.dt_reject_all():
            return False

        if dt_pivot == cls.dt_always_outdated():
            return False

        if v_pair2is_cmp_satisfied(dt, dt_pivot, cmp_s=">="):
            return True

        return False

    @classmethod
    def filepath2dt_mtime(cls,
                          filepath_in,
                          empty_file_allowed=False,
                          ):
        if empty_file_allowed is None: empty_file_allowed = False

        if not os.path.isfile(filepath_in):
            return cls.dt_always_outdated()

        st_size = os.stat(filepath_in).st_size
        if (not empty_file_allowed) and (st_size == 0):
            return cls.dt_always_outdated()

        mtime = os.path.getmtime(filepath_in)
        dt_utc = PytzTool.localize(datetime.utcfromtimestamp(mtime),
                               pytz.utc,
                               )

        return dt_utc

    @classmethod
    def filepath2is_uptodate(cls,
                             filepath,
                             pivot_datetime,
                             empty_file_allowed=False,
                             ):
        if pivot_datetime == cls.dt_reject_all():
            dt_mtime = cls.dt_always_outdated()
        else:
            dt_mtime = cls.filepath2dt_mtime(filepath, empty_file_allowed=empty_file_allowed,)

        is_uptodate = cls.dt2is_uptodate(dt_mtime, pivot_datetime)
        return is_uptodate


class DirTool:
    @classmethod
    def makedirs_if_empty(cls, dirpath):
        if not os.path.exists(dirpath): os.makedirs(dirpath)


class PathTool:
    @staticmethod
    def path2descendent_file_paths(source: Path) -> [Path]:
        yield from filter(lambda path: not path.is_dir(), source.rglob("*"))


filepath2utf8 = FileTool.filepath2utf8
filepath2utf8_lines = FileTool.filepath2utf8_lines
makedirs_if_empty = DirTool.makedirs_if_empty
utf82file = FileTool.utf82file
