import codecs
import os
import sys
from functools import reduce

from datetime import datetime

import pytz

from foxylib.tools.compare.compare_tools import v_pair2is_cmp_satisfied
from foxylib.tools.date.pytz_tools import pytz_localize
from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.string.string_tools import str2strip


class FileToolkit:
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
            f_open = lambda filepath: open(filepath, "wb")

        OUT_DIR = os.path.dirname(filepath)
        if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
        if os.path.islink(filepath): os.unlink(filepath)

        with f_open(filepath) as f:
            f.write(bytes)

    @classmethod
    def utf82file(cls, utf8,
                  filepath,
                  encoding="utf-8",
                  f_open=None,
                  ):
        logger = FoxylibLogger.func2logger(cls.utf82file)

        if f_open is None:
            f_open = lambda filepath: codecs.open(filepath, "w", encoding=encoding)

        OUT_DIR = os.path.dirname(filepath)
        if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
        if os.path.islink(filepath): os.unlink(filepath)

        with f_open(filepath) as f:
            if utf8:
                print(utf8, file=f)

    @classmethod
    def dirpath2mkdirs(cls, dirpath):
        if os.path.exists(dirpath):
            return

        os.makedirs(dirpath)

    @classmethod
    def writeln(cls, fptr, s):
        fptr.write("{}\n".format(s))


    @classmethod
    def filepath2is_empty(cls, filepath):
        return os.stat(filepath).st_size == 0

class FileTimeToolkit:
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

        if not os.path.isfile(filepath_in): return cls.dt_always_outdated()
        st_size = os.stat(filepath_in).st_size
        if (not empty_file_allowed) and (st_size == 0): return cls.dt_always_outdated()

        mtime = os.path.getmtime(filepath_in)
        dt_utc = pytz_localize(datetime.utcfromtimestamp(mtime),
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
            dt_mtime = cls.filepath2dt_mtime(filepath,
                                                       empty_file_allowed=empty_file_allowed,
                                                       )

        is_uptodate = cls.dt2is_uptodate(dt_mtime, pivot_datetime)
        return is_uptodate

class DirToolkit:
    @classmethod
    def makedirs_if_empty(cls, dirpath):
        if not os.path.exists(dirpath): os.makedirs(dirpath)

filepath2utf8 = FileToolkit.filepath2utf8
filepath2utf8_lines = FileToolkit.filepath2utf8_lines
makedirs_if_empty = DirToolkit.makedirs_if_empty
utf82file = FileToolkit.utf82file
