import logging
import os
import pickle

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class PickleReadwriterTool:
    @classmethod
    def filepath2read(cls, filepath):
        logger = FoxylibLogger.func_level2logger(cls.filepath2read, logging.DEBUG)
        logger.debug({"filepath": filepath})

        if not os.path.exists(filepath):
            return None

        bytes = FileTool.filepath2bytes(filepath)
        # logger.debug({"bytes":bytes})
        obj = pickle.loads(bytes)
        return obj

    @classmethod
    def obj_filepath2write(cls, obj, filepath):
        bytes = pickle.dumps(obj)
        FileTool.bytes2file(bytes, filepath)


class PickleReadwriter:
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        return PickleReadwriterTool.filepath2read(self.filepath)

    def write(self, obj):
        return PickleReadwriterTool.obj_filepath2write(obj, self.filepath)
