import locale
import os
from locale import getlocale

import pytest
from functools import lru_cache
from gettext import translation
from unittest import TestCase

from foxylib.tools.locale.locale_tool import LocaleTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

# $PYGETTEXT -d base -o locales/test_locale_tool.pot test_locale_tool.py
# $MSGFMT_PY -o base.mo base

class MyLocale:
    @classmethod
    @lru_cache(maxsize=2)
    def translation_ko(cls,):
        localedir = os.path.join(FILE_DIR, "locales")
        t = translation('test_locale_tool', localedir=localedir, languages=['ko'], fallback=True)
        return t

    @classmethod
    def gettext_ko(cls, *_, **__):
        t = cls.translation_ko()
        return t.gettext(*_, **__)

    @classmethod
    @lru_cache(maxsize=256)
    def lang2translation(cls, lang):
        localedir = os.path.join(FILE_DIR, "locales")
        t = translation('test_locale_tool', localedir=localedir, languages=[lang], fallback=True)
        return t

    @classmethod
    def gettext(cls, *_, **__):
        loc = locale.getlocale()
        lang = LocaleTool.locale2lang(loc)
        t = cls.lang2translation(lang)

        # t = cls.translation()
        return t.gettext(*_, **__)

class TestLocaleTool(TestCase):

    def test_01(self):
        with LocaleTool.override("en_US"):
            self.assertEqual(MyLocale.gettext("hello"), "hello")

        with LocaleTool.override("ko_KR"):
            self.assertEqual(MyLocale.gettext("goodbye"), "안녕")


    @pytest.mark.skip(reason="something wrong")
    def test_02(self):
        with LocaleTool.override("en_US"):
            """
            why translate here?
            """
            self.assertEqual(MyLocale.gettext_ko("hello"), "hello")

        with LocaleTool.override("ko_KR"):
            self.assertEqual(MyLocale.gettext_ko("goodbye"), "안녕")
