import io
import os

from foxylib.tools.file.file_tool import FileTool


class FormdataTool:
    @classmethod
    def filepath2item(cls, filepath):
        # https://stackoverflow.com/a/35712344
        bytes = FileTool.filepath2bytes(filepath)
        basename = os.path.basename(filepath)

        return io.BytesIO(bytes), basename
