import logging
import math

from nose.tools import assert_equal, assert_true

from foxylib.tools.collections.collections_tool import lchain
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import is_not_none
from foxylib.tools.number.number_tool import NumberTool


class TournamentTool:
    @classmethod
    def roundsize2rank_indexes_old(cls, n):
        """
        https://math.stackexchange.com/questions/515492/tournament-bracket-match-number-formula
        """
        r = NumberTool.int2log2_upper(n)

        result = [0]*n

        for p in range(r):
            for i in range(n):
                myrank = i // 2 ** p + 1
                result[i] += ((myrank % 4) // 2) * (2 ** (r - p - 1))

        return result

    @classmethod
    def roundsize2rank_indexes(cls, roundsize):
        logger = FoxylibLogger.func_level2logger(
                     cls.roundsize2rank_indexes, logging.DEBUG)

        n = 2**NumberTool.int2log2_upper(roundsize)
        ll_all = [[i] for i in range(n)]

        def ll2rank_indexes(ll_in):
            # logger.debug({'ll_in':ll_in})

            r = len(ll_in)
            if r == 1:  # final
                return list(map(lambda x: x if x < roundsize else None,
                                ll_in[0]))

            ll_next = [lchain(ll_in[j], ll_in[r-1-j]) for j in range(r//2)]
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
        if sorted(indexes_notnull) != list(range(n+1)):
            logger.debug({'sorted(indexes)':sorted(indexes),
                          'indexes': indexes,
                          'n':n,
                          })
            return False

        p = math.ceil(len(indexes) / 2)
        indexes_winner = [min(filter(is_not_none, indexes[2 * i:2 * (i + 1)]))
                          for i in range(math.ceil(len(indexes) / 2))]

        return cls.rank_indexes2is_correct(indexes_winner)

