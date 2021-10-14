import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pprint import pformat
from typing import Optional, Callable

from cachetools import LRUCache
from nose.tools import assert_is_not_none

from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.collections.collections_tool import lchain, DictTool, \
    merge_dicts, l_singleton2obj
from future.utils import lmap

from foxylib.tools.collections.groupby_tool import GroupbyTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import StringTool


class FulltextMatcher:
    def __init__(self, dict_value2texts, config:Optional["FulltextMatcher.Config"]=None):
        self.dict_value2texts = dict_value2texts or {}
        self.config: "FulltextMatcher.Config" = config

        def warmup():
            self.dict_norm2values()
        warmup()

    def __repr__(self):
        return str(self.__dict__)

    @dataclass(frozen=True)
    class Config:
        normalizer: Callable

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1),)
    def dict_norm2values(self):
        logger = FoxylibLogger.func_level2logger(self.dict_norm2values, logging.DEBUG)

        dict_value2norms = DictTool.values2mapped(self.dict_value2texts, self.text2norm)
        h_out = GroupbyTool.dicttree2reversed(dict_value2norms)
        return h_out

    def text2norm(self, text):
        normalizer = self.config.normalizer
        return normalizer(text) if normalizer else text

    def text2values(self, text):
        logger = FoxylibLogger.func_level2logger(self.text2values,
                                                 logging.DEBUG)

        h = self.dict_norm2values()
        values = h.get(self.text2norm(text)) or []

        return values

    def text2value(self, text):
        logger = FoxylibLogger.func_level2logger(self.text2value, logging.DEBUG)

        values = self.text2values(text)
        if not values:
            return None

        return l_singleton2obj(values)

