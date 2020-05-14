import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.socialmedia.discord.discord_tool import DiscordTool


class TestDiscordTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        text = "hello http://google.com/a/c no"

        hyp = DiscordTool.str2url_escaped(text)
        ref = "hello <http://google.com/a/c> no"

        # pprint(hyp)
        self.assertEqual(hyp, ref)
