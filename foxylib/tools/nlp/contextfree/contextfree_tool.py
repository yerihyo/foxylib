import logging
from itertools import product
from operator import itemgetter as ig

from future.utils import lmap
from nose.tools import assert_greater_equal

from foxylib.tools.collections.collections_tool import lchain, tchain
from foxylib.tools.collections.groupby_tool import gb_tree_global
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class ContextfreeTool:
    @classmethod
    def spans_list2j_tuples_reducible(cls, spans_list, f_gap2valid):
        logger = FoxylibLogger.func_level2logger(cls.spans_list2j_tuples_reducible, logging.DEBUG)
        f_self = cls.spans_list2j_tuples_reducible

        n = len(spans_list)
        assert_greater_equal(n, 1)

        if len(spans_list) == 1:
            spans = spans_list[0]
            for j in range(len(spans)):
                yield (j,)

        elif len(spans_list) == 2:
            spans1, spans2 = spans_list
            p1, p2 = len(spans1), len(spans2)

            for j1, j2 in product(range(p1), range(p2)):
                span_gap = (spans1[j1][1], spans2[j2][0],)
                is_valid = f_gap2valid(span_gap)
                logger.debug({"span_gap": span_gap,
                              "is_valid": is_valid,
                              })

                if is_valid:
                    yield (j1, j2)
        else:
            j_pairs_head = list(f_self(spans_list[:2], f_gap2valid))
            j1_list_valid = lmap(ig(1), j_pairs_head)

            spans1_filtered = lmap(lambda _j1: spans_list[1][_j1], j1_list_valid)
            spans_list_tail_filtered = lchain([spans1_filtered], spans_list[2:])

            j_tuples_tail_filtered = list(f_self(spans_list_tail_filtered, f_gap2valid))

            logger.debug({"j_pairs_head": j_pairs_head,
                          "j1_list_valid": j1_list_valid,
                          "spans1_filtered": spans1_filtered,
                          "spans_list_tail_filtered": spans_list_tail_filtered,
                          "j_tuples_tail_filtered": j_tuples_tail_filtered,

                          })

            h_j1_to_j_tuples_tail_filtered = {j1_list_valid[k1]: l
                                              for k1, l in gb_tree_global(j_tuples_tail_filtered, [ig(0)])}
            # j_tuples_tail = [(j1_list_valid[j_tuple[0]],)+j_tuple[1:]
            #                  for j_tuple in j_tuples_tail_filtered]

            # h_j1_to_l = h_gb_tree(j_tuples_tail, [ig(0)])

            for j_pair in j_pairs_head:
                j_tuples_tail_filtered = h_j1_to_j_tuples_tail_filtered.get(j_pair[1], [])
                for j_tuple_tail_filtered in j_tuples_tail_filtered:
                    yield tchain(j_pair, j_tuple_tail_filtered[1:])



