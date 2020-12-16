import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.math.tournament.tournament_tool import TournamentTool


class TestTournamentTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        hyp = TournamentTool.roundsize2rank_indexes_old(32)
        ref = [0,16,
               24,8,
               12,28,
               20,4,
               6,22,
               30,14,
               10,               26,
               18,               2,
               3,               19,
               27,               11,
               15,               31,
               23,               7,
               5,               21,
               29,               13,
               9,               25,
               17,               1
               ]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        hyp = TournamentTool.roundsize2rank_indexes(32)
        ref = [0, 31,
               15, 16,
               7, 24,
               8, 23,
               3, 28,
               12, 19,
               4, 27,
               11, 20,
               1, 30,
               14, 17,
               6, 25,
               9, 22,
               2, 29,
               13, 18,
               5, 26,
               10, 21]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

        self.assertTrue(TournamentTool.rank_indexes2is_correct(hyp))

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        hyp = TournamentTool.roundsize2rank_indexes(25)
        ref = [0,
 None,
 15,
 16,
 7,
 24,
 8,
 23,
 3,
 None,
 12,
 19,
 4,
 None,
 11,
 20,
 1,
 None,
 14,
 17,
 6,
 None,
 9,
 22,
 2,
 None,
 13,
 18,
 5,
 None,
 10,
 21]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

        self.assertTrue(TournamentTool.rank_indexes2is_correct(hyp))
