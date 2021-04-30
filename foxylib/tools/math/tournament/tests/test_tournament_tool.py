import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.math.tournament.tourney_tool import TourneyTool


class TestTourneyTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        hyp = TourneyTool.roundsize2rank_indexes_old(32)
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

        hyp = TourneyTool.roundsize2rank_indexes(32)
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

        self.assertTrue(TourneyTool.rank_indexes2is_correct(hyp))

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        hyp = TourneyTool.roundsize2rank_indexes(25)
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

        self.assertTrue(TourneyTool.rank_indexes2is_correct(hyp))

    def test_04(self):
        self.assertEqual(TourneyTool.roundsize2match_indexspan(64, 64), (0, 32), )
        self.assertEqual(TourneyTool.roundsize2match_indexspan(64, 32), (32, 48), )

    def test_05(self):
        self.assertEqual(TourneyTool.match_index2roundsize(4, 1), 4, )

        self.assertEqual(TourneyTool.match_index2roundsize(64, 0), 64, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 31), 64, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 32), 32, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 47), 32, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 48), 16, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 55), 16, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 56), 8, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 59), 8, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 60), 4, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 61), 4, )
        self.assertEqual(TourneyTool.match_index2roundsize(64, 62), 2, )

    def test_06(self):
        self.assertEqual(TourneyTool.match_count_created2match_count_with_child(64, 0), 0, )
        self.assertEqual(TourneyTool.match_count_created2match_count_with_child(64, 32), 0, )
        self.assertEqual(TourneyTool.match_count_created2match_count_with_child(64, 33), 2, )
        self.assertEqual(TourneyTool.match_count_created2match_count_with_child(64, 48), 32, )
        self.assertEqual(TourneyTool.match_count_created2match_count_with_child(64, 63), 62, )

    def test_07(self):
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 0), 32, )
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 1), 32, )
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 31), 32 + 32 // 2 - 1, )
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 42), 32 + 16 + (42 - 32 + 1 + 1) // 2 - 1, )
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 47), 32 + 16 + (47 - 32 + 1) // 2 - 1, )
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 55), 32 + 16 + 8 + (55 - 48 + 1) // 2 - 1, )
        self.assertEqual(TourneyTool.match_index2match_childindex(64, 61), 62, )

    def test_08(self):
        index2pair = lambda i: (i, i+1)

        self.assertEqual(TourneyTool.match_index2match_indexes_parent(2, 0), None, )
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 0), None, )
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 31), None, )
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 32), (0, 1), )
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 34), index2pair((34 - 32) * 2))
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 50), index2pair(32 + (50 - 32 - 16) * 2))
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 62), (60, 61))  # final
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 61), (58, 59))  # semifinal
        self.assertEqual(TourneyTool.match_index2match_indexes_parent(64, 60), (56, 57))  # semifinal

        with self.assertRaises(Exception):
            self.assertEqual(TourneyTool.match_index2match_indexes_parent(2, 1), None, )

    def test_09(self):
        self.assertEqual(
            list(TourneyTool.match_count2roundsize_count_pairs(64, 0)),
            []
        )
        self.assertEqual(
            list(TourneyTool.match_count2roundsize_count_pairs(64, 32)),
            [(64, 32), ]
        )

        self.assertEqual(
            list(TourneyTool.match_count2roundsize_count_pairs(64, 33)),
            [(64, 32), (32, 1)]
        )

        self.assertEqual(
            list(TourneyTool.match_count2roundsize_count_pairs(64, 55)),
            [(64, 32), (32, 16), (16, 7)]
        )

        self.assertEqual(
            list(TourneyTool.match_count2roundsize_count_pairs(64, 63)),
            [(64, 32), (32, 16), (16, 8), (8, 4), (4, 2), (2, 1)]
        )

    def test_10(self):
        self.assertEqual(TourneyTool.winner_count2match_count_vsknown(64, 0), 32)
        self.assertEqual(TourneyTool.winner_count2match_count_vsknown(64, 30), 32 + 15)
        self.assertEqual(TourneyTool.winner_count2match_count_vsknown(64, 31), 32 + 15)
        self.assertEqual(TourneyTool.winner_count2match_count_vsknown(64, 32), 32 + 16)
        self.assertEqual(TourneyTool.winner_count2match_count_vsknown(64, 44), 32 + 16 + 6)
