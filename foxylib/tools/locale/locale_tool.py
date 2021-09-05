import locale
import re
from gettext import translation

from functools import lru_cache

import threading
from contextlib import contextmanager

from future.utils import lmap

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.string.string_tool import str2lower, str2upper


class LocaleTool:
    # @classmethod
    # @contextmanager
    # # https://stackoverflow.com/questions/18593661/how-do-i-strftime-a-date-object-in-a-different-locale
    # def setlocale(cls, name):
    #     # LOCALE_LOCK = threading.Lock()
    #     # with LOCALE_LOCK:
    #     saved = locale.setlocale(locale.LC_ALL)
    #     try:
    #         yield locale.setlocale(locale.LC_ALL, name)
    #     finally:
    #         locale.setlocale(locale.LC_ALL, saved)

    # class Value:
    #     ko_KR = "ko_KR"
    #     ko = "ko"
    #     en = "en"

    @classmethod
    def locale2lang(cls, loc):
        if not loc:
            return loc

        return cls.locale2lang_country(loc)[0]

    @classmethod
    def locale2country(cls, loc):
        if not loc:
            return loc

        return cls.locale2lang_country(loc)[1]

    @classmethod
    def locale2langcode(cls, loc):
        if isinstance(loc,tuple):
            return loc[0]

        return loc

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern_delim(cls):
        return re.compile(r"[-_]")

    @classmethod
    def locale2lang_country(cls, loc):
        if not loc:
            return None, None

        langcode = cls.locale2langcode(loc)
        if langcode is None:
            return None, None

        l = cls.pattern_delim().split(langcode)
        return (str2lower(l[0]), str2upper(l[1]) if len(l)>=2 else None)

    @classmethod
    def lang_country2langcode(cls, lang, country):
        if not country:
            return lang

        return "_".join([lang,country])

    @classmethod
    def locale2is_english(cls, loc):
        return cls.contains_lang(["en",None], loc)

    @classmethod
    def contains_lang(cls, loc_list, loc):
        for _loc in loc_list:
            lang_01, lang_02 = lmap(lambda x: str2lower(cls.locale2lang(x)), [loc, _loc])
            if lang_01 == lang_02:
                return True
        return False

    @classmethod
    def locale_pair2has_same_language(cls, loc1, loc2):
        lang1 = cls.locale2lang(loc1)
        lang2 = cls.locale2lang(loc2)

        return str2lower(lang1) == str2lower(lang2)

    @classmethod
    @lru_cache(maxsize=1)
    def _locale_lock(cls):
        """
        not sure if lru_cache is thread safe
        """
        return threading.Lock()

    @classmethod
    @contextmanager
    def override(cls, loc, category=None):
        _category = category or locale.LC_ALL

        with cls._locale_lock():
            loc_prev = locale.setlocale(locale.LC_ALL)
            try:
                yield locale.setlocale(_category, locale=loc)
            finally:
                locale.setlocale(locale.LC_ALL, loc_prev)
