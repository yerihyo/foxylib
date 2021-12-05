import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pprint import pformat
from typing import Optional, Callable, TypeVar, List, Dict, Tuple, Pattern

from cachetools import LRUCache, cachedmethod
from nose.tools import assert_is_not_none

from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.collections.collections_tool import lchain, DictTool, \
    merge_dicts, l_singleton2obj
from future.utils import lmap

from foxylib.tools.collections.groupby_tool import GroupbyTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import AttributeTool
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import StringTool

T = TypeVar("T")


class StartswithMatcher:
    def __init__(self, dict_value2texts, config: Optional["StartswithMatcher.Config"] = None):
        self.dict_value2texts = dict_value2texts or {}
        self.config: "StartswithMatcher.Config" = config

        def warmup():
            self.pattern_value_list()
        warmup()

    def __repr__(self):
        return str(self.__dict__)

    @dataclass(frozen=True)
    class Config:
        normalizer: Callable

    def cachedict(self):
        return AttributeTool.get_or_init(self, '_cachedict', {})

    # @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1),)
    @cachedmethod(
        lambda x: DictTool.get_or_lazyinit(
            x.cachedict(),
            FunctionTool.func2name(StartswithMatcher.pattern_value_list),
            lambda: LRUCache(maxsize=1),
        ),
    )
    def pattern_value_list(self) -> List[Tuple[Pattern[str], T]]:
        logger = FoxylibLogger.func_level2logger(self.pattern_value_list, logging.DEBUG)

        def texts2pattern(texts: List[str]) -> Pattern[str]:
            # logger.debug({'texts':texts})
            norms = lmap(self.text2norm, texts)
            rstr_or = RegexTool.rstrs2or(lmap(re.escape, norms))
            rstr_bounded = RegexTool.rstr2bounded(rstr_or, r"^", RegexTool.right_wordbounds(), )
            return re.compile(rstr_bounded)

        pattern_value_list = [(texts2pattern(texts), value)
                              for value, texts in self.dict_value2texts.items()]
        return pattern_value_list

    def text2norm(self, text):
        normalizer = self.config.normalizer
        return normalizer(text) if normalizer else text

    def text2value(self, text):
        logger = FoxylibLogger.func_level2logger(self.text2value, logging.DEBUG)

        pattern_value_list = self.pattern_value_list()
        # logger.debug(pformat({
        #     'pattern_value_list': pattern_value_list,
        # }))

        text_norm = self.text2norm(text)
        for p, value in pattern_value_list:
            m = p.match(text_norm)
            if m:
                return value

        return None

