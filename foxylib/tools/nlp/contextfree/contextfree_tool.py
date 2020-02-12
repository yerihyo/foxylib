import logging
from itertools import product
from operator import itemgetter as ig

from future.utils import lmap, lrange
from nose.tools import assert_greater_equal, assert_true

from foxylib.tools.collections.collections_tool import lchain, tchain
from foxylib.tools.collections.groupby_tool import gb_tree_global, h_gb_tree
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class ContextfreeTool:
    @classmethod
    def spans_list2index_tuple_iter_reducible(cls, spans_list, gap2is_valid):
        n = len(spans_list)
        assert_greater_equal(n, 1)

        m0 = len(spans_list[0])
        j0_list_valid = lrange(m0)

        return cls._spans_list_j0_list2index_tuple_iter_reducible(spans_list, gap2is_valid, j0_list_valid)

    @classmethod
    def _spans_list_j0_list2index_tuple_iter_reducible(cls, spans_list, gap2is_valid, j0_list_valid):
        # logger = FoxylibLogger.func_level2logger(cls._spans_list_j0_list2index_tuple_iter_reducible, logging.DEBUG)
        f_self = cls._spans_list_j0_list2index_tuple_iter_reducible

        n = len(spans_list)
        assert_greater_equal(n, 1)
        assert_true(all(map(lambda j0: j0 < len(spans_list[0]), j0_list_valid)))

        if len(spans_list) == 1:
            for j in j0_list_valid:
                yield (j,)

        elif len(spans_list) == 2:
            spans0,spans1 = spans_list
            m1 = len(spans1)

            for j0, j1 in product(j0_list_valid, range(m1)):
                if cls.span_pair2is_reducible(spans0[j0], spans1[j1], gap2is_valid):
                    yield (j0, j1)

        else:
            j_pairs_head = list(f_self(spans_list[:2], gap2is_valid, j0_list_valid))
            j1_list_valid = lmap(ig(1), j_pairs_head)

            # spans_list_tail_filtered = cls._j1_list_valid2spans_list_tail(spans_list, j1_list_valid)
            j_tuples_tail = list(f_self(spans_list[1:], gap2is_valid, j1_list_valid, ))

            h_j1_to_j_tuples_tail = h_gb_tree(j_tuples_tail, [ig(0)])

            for j_pair in j_pairs_head:
                j_tuples_tail = h_j1_to_j_tuples_tail.get(j_pair[1], [])
                for j_tuple_tail in j_tuples_tail:
                    yield tchain(j_pair, j_tuple_tail[1:])

    # @classmethod
    # def _j1_list_valid2spans_list_tail(cls, spans_list, j1_list_valid):
    #     logger = FoxylibLogger.func_level2logger(cls._j1_list_valid2spans_list_tail, logging.DEBUG)
    #
    #     spans1_filtered = lmap(lambda j1: spans_list[1][j1], j1_list_valid)
    #     spans_list_tail_filtered = lchain([spans1_filtered], spans_list[2:])
    #
    #     logger.debug({#"j_pairs_head": j_pairs_head,
    #                   "j1_list_valid": j1_list_valid,
    #                   "spans1_filtered": spans1_filtered,
    #                   "spans_list_tail_filtered": spans_list_tail_filtered,
    #                   # "j_tuples_tail_filtered": j_tuples_tail_filtered,
    #                   })
    #
    #     return spans_list_tail_filtered

    # @classmethod
    # def _j1_list_valid2h_j1_to_j2_tuples_tail(cls, j_tuples_tail_filtered, j1_list_valid):
    #     return {j1_list_valid[k1]: j1_tuples_tail[1:]
    #             for k1, j1_tuples_tail in gb_tree_global(j_tuples_tail_filtered, [ig(0)])}
    #



    @classmethod
    def span_pair2is_reducible(cls, span1, span2, gap2is_valid):
        logger = FoxylibLogger.func_level2logger(cls.span_pair2is_reducible, logging.DEBUG)

        span_gap = (span1[1], span2[0],)
        is_valid = gap2is_valid(span_gap)
        logger.debug({"span_gap": span_gap,
                      "is_valid": is_valid,
                      })
        return is_valid