import locale
from contextlib import contextmanager

from foxylib.tools.string.string_tools import str2lower, str2upper


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


    @classmethod
    def locale2lang(cls, locale):
        if not locale:
            return locale

        return cls.locale2lang_country(locale)[0]

    @classmethod
    def locale2country(cls, locale):
        if not locale:
            return locale

        return cls.locale2lang_country(locale)[1]

    @classmethod
    def locale2lang_country(cls, locale):
        if not locale:
            return None, None

        l = locale.split("-")
        return (str2lower(l[0]), str2upper(l[1]) if len(l)>=2 else None)

    @classmethod
    def lang_country2locale(cls, lang, country):
        if not country:
            return lang

        return "-".join([lang,country])

    @classmethod
    def locale2is_english(cls, locale):
        return cls.contains_lang(["en",None], locale)

    @classmethod
    def contains_lang(cls, locale_list, locale):
        for _locale in locale_list:
            lang_01, lang_02 = lmap(lambda x: str2lower(cls.locale2lang(x)), [locale, _locale])
            if lang_01 == lang_02:
                return True
        return False

    @classmethod
    def locale_pair2has_same_language(cls, locale1, locale2):
        lang1 = cls.locale2lang(locale1)
        lang2 = cls.locale2lang(locale2)

        return str2lower(lang1) == str2lower(lang2)