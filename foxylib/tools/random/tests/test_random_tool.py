import logging
from functools import partial
from pprint import pprint
from random import randint
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.random.random_tool import RandomTool


class TestRandomTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        x, y = RandomTool.lasvegas(
            lambda: (randint(1, 6), randint(1, 6)),
            lambda p: p[0] != p[1]
        )

        pprint({'x': x, 'y': y})
        self.assertNotEqual(x, y)
