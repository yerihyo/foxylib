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

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import StringTool


class FulltextMatcher:
    def __init__(self, dict_value2texts, config:Optional["FulltextMatcher.Config"]=None):
        self.dict_value2texts = dict_value2texts or {}
        self.config: "FulltextMatcher.Config" = config

    @dataclass(frozen=True)
    class Config:
        normalizer: Callable
        # class Key:
        #     NORMALIZER = "normalizer"

        # @classmethod
        # def config2normalizer(cls, config):
        #     return DictTool.lookup(config, cls.Key.NORMALIZER)

    @classmethod
    def dict2normalized(cls, dict_value2texts, normalizer):
        logger = FoxylibLogger.func_level2logger(cls.dict2normalized, logging.DEBUG)
        # logger.debug({"dict_value2texts":dict_value2texts})

        return {value: lmap(normalizer, texts)
                for value, texts in dict_value2texts.items()}

    @classmethod
    def dict2reversed(cls, dict_value2texts):
        """
        Logic below will...
        First, create list of {string:{string}} dictionaries. (string=>set)
        Then, merge_dicts will merge this list of dictionaries into a single dictionary
        When there is conflict on keys, merge_dicts will union the values (DictToolkit.VWrite.union).
        """
        dict_text2values = merge_dicts([{text: {value}}
                                       for value, texts in dict_value2texts.items()
                                       for text in texts],
                                      vwrite=DictTool.VWrite.union)

        return dict_text2values

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=2),)
    def _dict_text2values(self):
        logger = FoxylibLogger.func_level2logger(self._dict_text2values, logging.DEBUG)

        cls = self.__class__

        dict_value2texts = self.dict_value2texts
        normalizer = self.config.normalizer
        dict_value2norms = cls.dict2normalized(dict_value2texts, normalizer) if normalizer else dict_value2texts
        dict_norm2values = cls.dict2reversed(dict_value2norms)
        # logger.debug(pformat({
        #     'normalizer': normalizer,
        #     'dict_value2texts': dict_value2texts,
        #     "dict_value2norms": dict_value2norms,
        #     "dict_norm2values": dict_norm2values,
        # }))
        return dict_norm2values

    def warmup(self):
        self._dict_text2values()

    def text2values(self, text):
        logger = FoxylibLogger.func_level2logger(self.text2values,
                                                 logging.DEBUG)

        cls = self.__class__
        normalizer = self.config.normalizer
        text_norm = normalizer(text) if normalizer else text
        h = self._dict_text2values()
        values = h.get(text_norm) or []

        # logger.debug({"text":text, "text_norm":text_norm, 'h':h})

        return values

    def text2value(self, text):
        logger = FoxylibLogger.func_level2logger(self.text2value, logging.DEBUG)

        values = self.text2values(text)
        if not values:
            return None

        # logger.debug({'text':text, 'values':values})

        return l_singleton2obj(values)

