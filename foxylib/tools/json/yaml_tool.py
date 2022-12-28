import logging
from typing import Iterable, List, Union, Dict

import yaml

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key, DictTool
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class YamlTool:
    @classmethod
    def filepath2j(cls, filepath, Loader=None) -> Union[Dict,List,None]:
        logger = FoxylibLogger.func_level2logger(cls.filepath2j, logging.DEBUG)

        utf8 = FileTool.filepath2utf8(filepath)
        if utf8 is None:
            return None
        # logger.info({"utf8": utf8})
        if Loader is None:
            Loader = yaml.SafeLoader

        j = yaml.load(utf8, Loader=Loader)
        return j

    # @classmethod
    # def filepath2j_iter(cls, filepath, Loader=None) -> Iterable:
    #     # https://stackoverflow.com/a/49753925/1902064
    #     logger = FoxylibLogger.func_level2logger(cls.filepath2j_iter, logging.DEBUG)
    #
    #     # utf8 = FileTool.filepath2utf8(filepath)
    #     # logger.info({"utf8": utf8})
    #     if Loader is None:
    #         Loader = yaml.CSafeLoader
    #
    #     with open(filepath,) as f:
    #         for event in yaml.parse(f, Loader):
    #             yield event

    @classmethod
    def j_yaml2h_reversed(cls, j_yaml):
        h = merge_dicts([{v:k}
                         for k, l in j_yaml.items()
                         for v in l],
                        vwrite=vwrite_no_duplicate_key)
        return h

    @classmethod
    def j2filepath(cls, j, filepath, **kwargs_in):
        kwargs = merge_dicts([
            {'allow_unicode':True,
             'sort_keys':False,
             },
            kwargs_in,
        ], vwrite=DictTool.VWrite.overwrite)

        with open(filepath, 'w') as f:
            yaml.dump(j, f, **kwargs)
