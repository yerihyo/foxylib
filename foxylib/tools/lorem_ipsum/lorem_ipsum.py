#!/usr/bin/env python
import os

from foxylib.tools.file.file_tools import FileToolkit

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class LoremIpsum:
    @classmethod
    def lang2str(cls, lang):
        filepath = os.path.join(FILE_DIR,"{}.txt".format(lang))
        s = FileToolkit.filepath2utf8(filepath)
        return s
