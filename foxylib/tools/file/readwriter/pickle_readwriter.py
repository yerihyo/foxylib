import os
import pickle

from foxylib.tools.file.file_tool import FileTool


class PickleReadwriterTool:
    @classmethod
    def filepath2read(cls, filepath):
        if not os.path.exists(filepath):
            return None

        return pickle.loads(FileTool.filepath2bytes(filepath))

    @classmethod
    def obj_filepath2write(cls, obj, filepath):
        return FileTool.bytes2file(pickle.dumps(obj), filepath)


class PickleReadwriter:
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        return PickleReadwriterTool.filepath2read(self.filepath)

    def write(self, obj):
        return PickleReadwriterTool.obj_filepath2write(obj, self.filepath)
