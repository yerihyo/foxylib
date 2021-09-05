import logging
import re
from functools import lru_cache

from cachetools import LRUCache
from nose.tools import assert_is_not_none

from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.collections.collections_tool import lchain, DictTool, merge_dicts
from future.utils import lmap

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import StringTool


class GazetteerMatcher:
    def __init__(self, dict_value2texts, config=None):
        self.dict_value2texts = dict_value2texts or {}
        self.config = config

    class Config:
        class Key:
            NORMALIZER = "normalizer"
            TEXTS2PATTERN = "texts2pattern"

        @classmethod
        def config2normalizer(cls, config):
            return DictTool.lookup(config, cls.Key.NORMALIZER)

        @classmethod
        def config2pattern_generator(cls, config):
            return DictTool.lookup(config, cls.Key.TEXTS2PATTERN)

    @classmethod
    def append_value2texts(cls, dict_value2texts):
        return {value: lchain(texts, [value])
                for value, texts in dict_value2texts.items()}

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

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1),)
    def _dict_text2values(self):
        cls = self.__class__

        dict_value2texts = self.dict_value2texts
        normalizer = cls.Config.config2normalizer(self.config)
        dict_value2norms = cls.dict2normalized(dict_value2texts, normalizer) if normalizer else dict_value2texts
        return cls.dict2reversed(dict_value2norms)

    class Default:
        @classmethod
        def texts2regex(cls, texts):
            return RegexTool.rstrs2or(map(re.escape, texts))

        @classmethod
        def texts2pattern_word(cls, texts):
            regex_raw = cls.texts2regex(texts)
            regex_word = RegexTool.rstr2bounded(regex_raw, RegexTool.left_wordbounds(), RegexTool.right_wordbounds())
            return re.compile(regex_word, )  # re.I can be dealt with normalizer

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1), )
    def pattern(self):
        cls = self.__class__
        texts2pattern = cls.Config.config2pattern_generator(self.config) or cls.Default.texts2pattern_word
        return texts2pattern(self._dict_text2values().keys())

    def warmup(self):
        self.pattern()
        self._dict_text2values()

    def text2matches(self, text):
        cls = self.__class__

        normalizer = cls.Config.config2normalizer(self.config)
        text_norm = normalizer(text) if normalizer else text

        return self.pattern().finditer(text_norm)

    def match2span_value_iter(self, match):
        _dict_text2values = self._dict_text2values()
        for v in _dict_text2values[match.group()]:
            yield (match.span(), v,)

    def text2span_value_iter(self, text):
        matches = self.text2matches(text)
        for match in matches:
            yield from self.match2span_value_iter(match)

    def text2sub(self, text):
        span_value_list = list(self.text2span_value_iter(text))
        text_subbed = StringTool.str_spans2replace_all(text, span_value_list)
        return text_subbed
