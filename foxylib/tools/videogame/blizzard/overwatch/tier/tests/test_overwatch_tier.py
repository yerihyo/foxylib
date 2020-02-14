import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import URLTool
from foxylib.tools.videogame.blizzard.overwatch.tier.overwatch_tier import OverwatchTier


class TestOverwatchTier(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        j_gold = OverwatchTier.value2j(OverwatchTier.V.GOLD)

        self.assertTrue(j_gold)
        self.assertEqual(OverwatchTier.j_lang2name(j_gold, "en"), "Gold")
        self.assertEqual(OverwatchTier.j_lang2name(j_gold, "ko"), "골드")

        self.assertTrue(URLTool.url2is_accessible(OverwatchTier.j2image_url(j_gold)))


    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        j_tier_list = OverwatchTier.j_list_all()
        for j_tier in j_tier_list:
            self.assertTrue(URLTool.url2is_accessible(OverwatchTier.j2image_url(j_tier)))