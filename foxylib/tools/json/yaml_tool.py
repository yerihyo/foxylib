import yaml

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class YAMLTool:
    @classmethod
    def filepath2j(cls, filepath, loader=None):
        logger = FoxylibLogger.func2logger(cls.filepath2j)

        utf8 = FileTool.filepath2utf8(filepath)
        # logger.info({"utf8": utf8})
        if loader is None:
            loader = yaml.SafeLoader

        j = yaml.load(utf8, Loader=loader)
        return j

    @classmethod
    def j_yaml2h_reversed(cls, j_yaml):
        h = merge_dicts([{v:k}
                         for k, l in j_yaml.items()
                         for v in l],
                        vwrite=vwrite_no_duplicate_key)
        return h
