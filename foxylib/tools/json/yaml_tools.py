import yaml

from foxylib.tools.file_tools import FileToolkit


class YAMLToolkit:
    @classmethod
    def filepath2j(cls, filepath):
        utf8 = FileToolkit.filepath2utf8(filepath)
        j = yaml.load(utf8)
        return j