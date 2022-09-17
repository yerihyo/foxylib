import os
from abc import ABCMeta, abstractmethod
from datetime import datetime

from nose.tools import assert_is_not_none

from foxylib.tools.csv.csv_tool import CsvTool
from foxylib.tools.file.file_tool import FileTool, FiletimeTool
from foxylib.tools.json.yaml_tool import YamlTool


class FileReadwriterTool:
    @classmethod
    def filepath2iostream(cls, filepath,):  # naive
        class Readwriter:
            @classmethod
            def write(cls, bytes):
                FileTool.makedirs_or_skip(os.path.dirname(filepath))
                FileTool.bytes2file(bytes, filepath)

            @classmethod
            def read(cls, ):
                if not os.path.exists(filepath):
                    raise FileNotFoundError()

                return FileTool.filepath2bytes(filepath)

        return Readwriter

    @classmethod
    def _iostream2encoding_wrapped(cls, iostream_in, encoding):  # naive
        class Readwriter:
            @classmethod
            def write(cls, utf8):
                iostream_in.write(utf8.encode(encoding))

            @classmethod
            def read(cls, ):
                return iostream_in.read().decode(encoding)

        return Readwriter

    @classmethod
    def _iostream2utf8_wrapped(cls, iostream_in):  # naive
        return cls._iostream2encoding_wrapped(iostream_in, 'utf-8')

    @classmethod
    def filepath2utf8_readwriter(cls, filepath):  # naive
        iostream = cls.filepath2iostream(filepath)
        readwriter = cls._iostream2utf8_wrapped(iostream)
        return readwriter

    @classmethod
    def readwriter2wrapped_csv(cls, readwriter, encoding):
        raise NotImplementedError()

    @classmethod
    def filepath2yaml_readwriter(cls, filepath):
        class Readwriter:
            @classmethod
            def write(cls, jdoc_yaml):
                YamlTool.j2filepath(jdoc_yaml, filepath)

            @classmethod
            def read(cls,):
                return YamlTool.filepath2j(filepath)

        return Readwriter

    @classmethod
    def filepath2csv_readwriter(cls, filepath):
        class Readwriter:
            @classmethod
            def write(cls, str_ll):
                CsvTool.strs_iter2file(str_ll, filepath)

            @classmethod
            def read(cls, ):
                return CsvTool.filepath2str_ll(filepath)

        return Readwriter

