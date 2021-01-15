import os
import shutil

from foxylib.tools.file.file_tool import FileTool


class Lines2fileCache:
    """
    Need to change later using coroutine
    """

    def __init__(self, key2filepath_out, key2filepath_tmp):
        self.key2filepath_out = key2filepath_out
        self.key2filepath_tmp = key2filepath_tmp

    def __getitem__(self, k):
        filepath_out = self.key2filepath_out(k)

        if not os.path.exists(filepath_out):
            raise KeyError

        lines = list(FileTool.filepath2utf8_lines(filepath_out))
        return lines

    def __setitem__(self, k, lines):
        line_list = list(lines)

        filepath_out = self.key2filepath_out(k)
        filepath_tmp = self.key2filepath_tmp(k)

        if not line_list:
            if os.path.exists(filepath_out):
                os.remove(filepath_out)
            return

        FileTool.makedirs_or_skip(os.path.dirname(filepath_out))
        FileTool.makedirs_or_skip(os.path.dirname(filepath_tmp))

        FileTool.lines2file(line_list, filepath_tmp)
        shutil.move(filepath_tmp, filepath_out)
