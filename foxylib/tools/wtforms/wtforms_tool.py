from functools import lru_cache

from wtforms.i18n import DummyTranslations

class WTFormsTool:
    @classmethod
    @lru_cache(maxsize=2)
    def dummy_translation(cls):
        return DummyTranslations()

    @classmethod
    def h_gettext2translations(cls, h_gettext):
        class Translations(DummyTranslations):
            def gettext(self, str_in):
                if str_in in h_gettext:
                    return h_gettext[str_in]

                return super(Translations).gettext(str_in)
        return Translations()
