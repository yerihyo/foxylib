import os
from datetime import datetime

from nose.tools import assert_is_not_none

from foxylib.tools.file.file_tool import FileTool, FiletimeTool


class ReadwriterTool:
    @classmethod
    def file2is_valid(cls, filepath, timedelta_pivot):
        if not os.path.exists(filepath):
            return False

        if timedelta_pivot is None:
            return True

        dt_mtime = FiletimeTool.filepath2dt_mtime(filepath)
        assert_is_not_none(dt_mtime)

        return dt_mtime > datetime.now() - timedelta_pivot

    @classmethod
    def filepath2readwriter(cls, filepath, timedelta_pivot):  # naive
        class Readwriter:
            @classmethod
            def write(cls, bytes):
                FileTool.makedirs_or_skip(os.path.dirname(filepath))
                FileTool.bytes2file(bytes, filepath)

            @classmethod
            def is_valid(cls, ):
                return ReadwriterTool.file2is_valid(filepath, timedelta_pivot)

            @classmethod
            def read(cls, ):
                if not cls.is_valid():
                    raise KeyError()

                return FileTool.filepath2bytes(filepath)

        return Readwriter

    @classmethod
    def readerwriter2wrapped_encoding(cls, readwriter, encoding):  # naive
        class Readwriter:
            @classmethod
            def write(cls, utf8):
                readwriter.write(utf8.encode(encoding))

            @classmethod
            def is_valid(cls, ):
                return readwriter.is_valid()

            @classmethod
            def read(cls, ):
                if not cls.is_valid():
                    raise KeyError()

                return readwriter.read().decode(encoding)

        return Readwriter

    @classmethod
    def readerwriter2wrapped_utf8(cls, readwriter):  # naive
        return cls.readerwriter2wrapped_encoding(readwriter, 'utf-8')

    @classmethod
    def readerwriter2wrapped_csv(cls, readwriter, encoding):
        raise NotImplementedError()

