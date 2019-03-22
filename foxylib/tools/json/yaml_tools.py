import yaml

from foxylib.tools.file.file_tools import FileToolkit
from foxylib.tools.log.logger_tools import FoxylibLogger


class YAMLToolkit:
    @classmethod
    def filepath2j(cls, filepath):
        logger = FoxylibLogger.func2logger(cls.filepath2j)

        utf8 = FileToolkit.filepath2utf8(filepath)
        # logger.info({"utf8": utf8})

        j = yaml.load(utf8)
        return j

