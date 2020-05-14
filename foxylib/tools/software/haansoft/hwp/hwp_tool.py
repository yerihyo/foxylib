# reference: https://www.hancom.com/etc/hwpDownload.do

import logging
import sys
from contextlib import closing
from functools import lru_cache
from io import BytesIO
from tempfile import NamedTemporaryFile

from hwp5.dataio import ParseError
from hwp5.errors import InvalidHwp5FileError
from hwp5.hwp5txt import TextTransform
from hwp5.utils import make_open_dest_file
from hwp5.xmlmodel import Hwp5File

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool


class HWPTool:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def _text_transform(cls):
        return TextTransform()


    @classmethod
    def bytes2text(cls, bytes):
        with NamedTemporaryFile() as f:
            f.write(bytes)
            return cls.filepath2text(f.name)

    @classmethod
    def filepath2text(cls, filepath_hwp):
        logger = FoxylibLogger.func_level2logger(cls.filepath2text, logging.DEBUG)
        tt = cls._text_transform()

        try:
            with closing(Hwp5File(filepath_hwp)) as hwp5file:
                with BytesIO() as bytes_io:
                    tt.transform_hwp5_to_text(hwp5file, bytes_io)

                    # https://stackoverflow.com/questions/26879981/writing-then-reading-in-memory-bytes-bytesio-gives-a-blank-result
                    bytes_io.seek(0)
                    bytes = bytes_io.read()

                    return bytes.decode('UTF-8')

        except ParseError as e:
            e.print_to_logger(logger)
            raise
        except InvalidHwp5FileError as e:
            logger.error('%s', e)
            raise

    @classmethod
    @VersionTool.inactive(reason="Unnecessary because cls.filepath2text works")
    def filepath2textfile(cls, filepath_hwp, filepath_text):
        logger = FoxylibLogger.func_level2logger(cls.filepath2textfile, logging.DEBUG)

        text_transform = TextTransform()

        open_dest = make_open_dest_file(filepath_text)
        transform = text_transform.transform_hwp5_to_text

        try:
            with closing(Hwp5File(filepath_hwp)) as hwp5file:
                with open_dest() as dest:
                    transform(hwp5file, dest)
        except ParseError as e:
            e.print_to_logger(logger)
        except InvalidHwp5FileError as e:
            logger.error('%s', e)
            sys.exit(1)


