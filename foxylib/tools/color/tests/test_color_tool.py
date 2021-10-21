import logging
from pprint import pformat
from unittest import TestCase

from foxylib.tools.color.color_tool import ColorTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestColorTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        logger = FoxylibLogger.func_level2logger(self.test_1, logging.DEBUG)

        rgb_tinted = ColorTool.rgb2tinted((173, 216, 230), 0.5)
        logger.debug(pformat({'rgb_tinted': rgb_tinted}))
        self.assertEqual(rgb_tinted, None)
