import logging
import math
from pprint import pformat
from typing import Tuple, List

from future.utils import lmap
from nose.tools import assert_equal, assert_true, assert_less_equal, assert_less, assert_greater_equal

from foxylib.tools.collections.collections_tool import lchain, tmap
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import is_not_none
from foxylib.tools.number.number_tool import NumberTool


class TourneyTool:

    class Constant:
        ROUNDSIZE_FINAL = 2

    @classmethod
    def player_count2round_count(cls, player_count):
        return NumberTool.int2log2_upper(player_count)

    @classmethod
    def roundsize2rank_indexes_old(cls, n):
        """
        https://math.stackexchange.com/questions/515492/tournament-bracket-match-number-formula
        """
        r = NumberTool.int2log2_upper(n)

        result = [0] * n

        for p in range(r):
            for i in range(n):
                myrank = i // 2 ** p + 1
                result[i] += ((myrank % 4) // 2) * (2 ** (r - p - 1))

        return result

    @classmethod
    def roundsize2rank_indexes(cls, roundsize):
        logger = FoxylibLogger.func_level2logger(
            cls.roundsize2rank_indexes, logging.DEBUG)

        n = 2 ** NumberTool.int2log2_upper(roundsize)
        ll_all = [[i] for i in range(n)]

        def ll2rank_indexes(ll_in):
            # logger.debug({'ll_in':ll_in})

            r = len(ll_in)
            if r == 1:  # final
                return list(map(lambda x: x if x < roundsize else None,
                                ll_in[0]))

            ll_next = [lchain(ll_in[j], ll_in[r - 1 - j]) for j in range(r // 2)]
            return ll2rank_indexes(ll_next)

        rank_indexes = ll2rank_indexes(ll_all)
        return rank_indexes

    @classmethod
    def rank_indexes2is_correct(cls, indexes):
        logger = FoxylibLogger.func_level2logger(
            cls.roundsize2rank_indexes, logging.DEBUG)

        assert_true(indexes)
        indexes_notnull = list(filter(is_not_none, indexes))
        assert_true(indexes_notnull)

        if len(indexes) == 1 and indexes[0] == 0:
            return True

        n = max(indexes_notnull)
        if sorted(indexes_notnull) != list(range(n + 1)):
            logger.debug({'sorted(indexes)': sorted(indexes),
                          'indexes': indexes,
                          'n': n,
                          })
            return False

        p = math.ceil(len(indexes) / 2)
        indexes_winner = [min(filter(is_not_none, indexes[2 * i:2 * (i + 1)]))
                          for i in range(math.ceil(len(indexes) / 2))]

        return cls.rank_indexes2is_correct(indexes_winner)

    @classmethod
    def roundsize2match_count(cls, roundsize):
        assert (NumberTool.is_power_of_two(roundsize))
        return roundsize // 2

    @classmethod
    def match_index2round_index(cls, player_count, match_index):
        round_index, _ = cls.match_index2round_index_game_index(player_count, match_index)
        return round_index

    @classmethod
    def match_index2round_index_game_index(cls, player_count, match_index):
        if not TourneyTool.player_count2is_operatable(player_count):
            return None, None

        """ player_count is roundsize """
        assert (NumberTool.is_power_of_two(player_count))
        assert_less(match_index, player_count - 1)

        if match_index < player_count // 2:
            return 0, match_index

        round_index_prev, game_index = cls.match_index2round_index_game_index(
            player_count // 2,  # half advance to the next round
            match_index - player_count // 2,  # half == # players dropped == # matches played
        )
        return round_index_prev + 1, game_index

    @classmethod
    def match_index2roundsize(cls, player_count, match_index):
        """ player_count is roundsize """
        if not TourneyTool.player_count2is_operatable(player_count):
            return None

        round_index = cls.match_index2round_index(player_count, match_index)
        return cls.round_index2roundsize(player_count, round_index)

    @classmethod
    def roundsize2match_indexspan(cls, player_count, roundsize):
        logger = FoxylibLogger.func_level2logger(cls.roundsize2match_indexspan, logging.DEBUG)

        assert_less_equal(roundsize, player_count)
        matchcount_round1 = cls.roundsize2match_count(player_count)

        if roundsize == player_count:
            return 0, matchcount_round1

        if roundsize < player_count:
            span_higherround = cls.roundsize2match_indexspan(player_count // 2, roundsize)
            # logger.debug({'span_higherround':span_higherround,
            #               'matchcount_lowest':matchcount_lowest,})

            return tmap(lambda x: matchcount_round1 + x, span_higherround)

        raise NotImplementedError(f"Should not come here -  player_count={player_count}, roundsize={roundsize}")

    @classmethod
    def match_count_created2match_count_with_child(cls, player_count, matchcount_created):
        """ player_count is roundsize """
        assert (NumberTool.is_power_of_two(player_count))

        roundsize = player_count
        matchcount_this = cls.roundsize2match_count(roundsize)
        return max(matchcount_created - matchcount_this, 0) * 2

    @classmethod
    def winner_count2match_count_vsknown(cls, player_count, winner_count):
        """ player_count is roundsize """
        assert (NumberTool.is_power_of_two(player_count))

        roundsize = player_count
        matchcount_this = cls.roundsize2match_count(roundsize)
        if winner_count <= matchcount_this:
            return matchcount_this + winner_count // 2

        count_plannable_child = cls.winner_count2match_count_vsknown(player_count//2, winner_count-matchcount_this)
        return matchcount_this + count_plannable_child

    @classmethod
    def match_index2match_childindex(cls, player_count, matchindex_in):
        assert (NumberTool.is_power_of_two(player_count))
        assert_less(matchindex_in, player_count-1)

        matchcount_round1 = cls.roundsize2match_count(player_count)

        if matchindex_in < matchcount_round1:
            return matchcount_round1 + matchindex_in // 2

        matchindex_out_next = cls.match_index2match_childindex(
            player_count // 2,
            matchindex_in - matchcount_round1,
        )
        return matchindex_out_next + matchcount_round1

    @classmethod
    def match_index2match_indexes_parent(cls, player_count, matchindex_in):
        logger = FoxylibLogger.func_level2logger(cls.match_index2match_indexes_parent, logging.DEBUG)
        # logger.debug({'player_count': player_count, 'matchindex_in':matchindex_in})
        assert (NumberTool.is_power_of_two(player_count))

        matchcount_round1 = cls.roundsize2match_count(player_count)
        if matchindex_in < matchcount_round1:
            return None

        matchcount_next = matchcount_round1 // 2
        if matchindex_in < matchcount_round1 + matchcount_next:
            matchsubindex_round2 = matchindex_in - matchcount_round1
            return (2 * matchsubindex_round2,
                    2 * matchsubindex_round2 + 1)

        matchindexes_out_next = cls.match_index2match_indexes_parent(
            player_count // 2,
            matchindex_in - matchcount_round1,
        )

        return tmap(lambda x: x+matchcount_round1, matchindexes_out_next)

    @classmethod
    def match_index2player_index_pair(
            cls,
            match_index: int,
            player_count: int,
            player_indexes_winner: List[int],
    ) -> Tuple[int, int]:
        logger = FoxylibLogger.func_level2logger(cls.match_index2player_index_pair, logging.DEBUG)

        match_indexes_parent = cls.match_index2match_indexes_parent(player_count, match_index)
        if match_indexes_parent is None:
            return match_index * 2, match_index * 2 + 1

        return tmap(lambda i: player_indexes_winner[i], match_indexes_parent)

    @classmethod
    def match_index2player_pair(cls, match_index, players, winners_prev):
        logger = FoxylibLogger.func_level2logger(cls.match_index2player_pair, logging.DEBUG)

        # logger.debug({
        #     'match_index': match_index,
        #     'len(players)': len(players),
        #     'len(winners_prev)': len(winners_prev),
        # })

        match_indexes_parent = cls.match_index2match_indexes_parent(len(players), match_index)
        if match_indexes_parent is None:
            return players[match_index*2:(match_index+1)*2]

        return lmap(lambda i: winners_prev[i], match_indexes_parent)


    @classmethod
    def match_count2roundsize_count_pairs(cls, player_count, matchcount_in):
        matchcount_round1 = cls.roundsize2match_count(player_count)
        matchcount_out_round1 = min(matchcount_round1, matchcount_in)

        if matchcount_out_round1 > 0:
            yield player_count, matchcount_out_round1

        if matchcount_in > matchcount_round1:
            yield from cls.match_count2roundsize_count_pairs(player_count//2, matchcount_in-matchcount_round1)

    @classmethod
    def round_index2roundsize(cls, player_count, round_index):
        assert (NumberTool.is_power_of_two(player_count))
        roundsize = player_count // 2 ** round_index
        assert_greater_equal(roundsize, 1)
        return roundsize

    @classmethod
    def player_count2match_count(cls, player_count):
        return max(player_count-1, 0)

    @classmethod
    def player_count2is_operatable(cls, player_count):
        return player_count >= 2

