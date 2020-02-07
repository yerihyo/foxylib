import logging
from unittest import TestCase

from future.utils import lfilter

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.videogame.overwatch.hero.overwatch_hero import OverwatchHero


class TestOverwatchHero(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        j_brigitte = OverwatchHero.codename2j(OverwatchHero.Codename.BRIGITTE)

        self.assertTrue(j_brigitte)
        self.assertEqual(OverwatchHero.j_lang2name(j_brigitte, "en"), "Brigitte")
        self.assertEqual(OverwatchHero.j_lang2name(j_brigitte, "ko"), "브리기테")