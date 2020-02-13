import logging
from asyncio import gather
from pprint import pprint
from unittest import TestCase

from foxylib.tools.asyncio.asyncio_tool import AsyncioTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.videogame.blizzard.overwatch.overwatch_tool import OwapiTool, OverwatchTool


class TestOwapiTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        j_blob = OwapiTool.battletag2j_blob("yeri#11211")

        logger.debug({"j_blob":j_blob})
        self.assertFalse({"kr","eu","us"} - set(j_blob.keys()))
