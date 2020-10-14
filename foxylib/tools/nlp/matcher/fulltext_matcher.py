import logging
import re
from functools import lru_cache

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
    def __init__(self, dict_value2texts, config=None):
        self.dict_value2texts = dict_value2texts or {}
        self.config = config

    class Config:
        class Key:
            NORMALIZER = "normalizer"

        @classmethod
        def config2normalizer(cls, config):
            return DictTool.lookup(config, cls.Key.NORMALIZER)

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
        cls = self.__class__

        dict_value2texts = self.dict_value2texts
        normalizer = cls.Config.config2normalizer(self.config)
        dict_value2norms = cls.dict2normalized(dict_value2texts, normalizer) if normalizer else dict_value2texts
        dict_norm2values = cls.dict2reversed(dict_value2norms)
        # raise Exception({
        #     "dict_value2norms":dict_value2norms,
        #     "dict_norm2values":dict_norm2values,
        # })
        return dict_norm2values

    def warmup(self):
        self._dict_text2values()

    def text2values(self, text):
        cls = self.__class__
        normalizer = cls.Config.config2normalizer(self.config)
        text_norm = normalizer(text) if normalizer else text
        values = self._dict_text2values().get(text_norm) or []
        return values

    def text2value(self, text):
        values = self.text2values(text)
        if not values:
            return None

        return l_singleton2obj(value)

