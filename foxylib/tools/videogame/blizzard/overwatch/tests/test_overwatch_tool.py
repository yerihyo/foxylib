import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.videogame.blizzard.overwatch.overwatch_tool import OwapiTool


class TestOwapiTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        j_stats = OwapiTool.battletag2j_stats("yeri#11211")

        logger.debug({"j_stats":j_stats})
        self.assertFalse({"kr","eu","us"} - set(j_stats.keys()))

        self.assertTrue(OwapiTool.j_stats2damage_comprank(j_stats))
        self.assertTrue(OwapiTool.j_stats2support_comprank(j_stats))
        self.assertTrue(OwapiTool.j_stats2tank_comprank(j_stats))

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)
        hyp = OwapiTool.battletag2exists("yeri#11212")

        self.assertFalse(hyp)
