import logging
import math

from operator import itemgetter as ig
from typing import Set, Tuple, List, Optional, TypeVar, Union, Literal, Iterable

from future.utils import lmap
from nose.tools import assert_less_equal, assert_is_not_none

from foxylib.tools.collections.collections_tool import lchain, tmap, merge_dicts, \
    DictTool, sfilter, AbsoluteOrder
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.number.number_tool import SignTool

T = TypeVar("T")


class SpanTool:
    @classmethod
    def is_in(cls, v, span):
        assert_is_not_none(span)

        if (not v) or (not span):  # empty span
            return False

        if (span[0] is not None) and (span[0] > v):
            return False

        if (span[1] is not None) and (v >= span[1]):
            return False

        return True

    # s, e = span
    # return s <= v <= e

    @classmethod
    def spans2span_covering(cls, spans: List[Tuple[T, T]]) -> Optional[Tuple[T, T]]:
        if not spans:
            return None

        lb = min(map(ig(0), spans))
        ub = max(map(ig(1), spans))
        return lb, ub

    @classmethod
    def steps(cls, start, end, step):
        logger = FoxylibLogger.func_level2logger(cls.steps, logging.DEBUG)

        x = start
        sign_init = SignTool.sign(end-start)

        if sign_init == 0:
            yield start
        else:
            sign_step = SignTool.sign(step)
            if sign_init != sign_step:
                raise RuntimeError(
                    {"sign_init": sign_init, 'sign_step': sign_step})

            while True:
                sign = SignTool.sign(end-x)

                # logger.debug({'x': x, 'start': start,
                #               'sign': sign, 'sign_init': sign_init})
                if sign != sign_init:
                    break

                yield x
                x = x + step

            yield end  # last value

    @classmethod
    def spans2nonoverlapping_greedy(cls, spans):
        span_list = sorted(spans)

        end = None
        for span in span_list:
            s, e = span
            if end is not None and end > s:
                continue

            yield span
            end = e

    @classmethod
    def span_pair2between(cls, span1, span2):
        s1, e1 = span1
        s2, e2 = span2

        assert_less_equal(s1, e1)
        assert_less_equal(s2, e2)

        if e1 <= s2:
            return e1, s2

        # if e2 <= s1:
        #     return e2, s1

        return None

    @classmethod
    def spans2is_consecutive(cls, spans):
        span_prev = None
        for span in spans:
            if span is None:
                return False

            if span_prev is None:
                span_prev = span
                continue

            if span_prev[1] + 1 != span[0]:
                return False

            span_prev = span
        return True

    @classmethod
    def is_adjacent(cls, span1, span2):
        return cls.spans2is_consecutive([span1, span2])

    @classmethod
    def overlaps(cls, se1, se2):
        if se1 is None:
            return False
        if se2 is None:
            return False

        s1, e1 = se1
        s2, e2 = se2

        if (e1 is not None) and (s2 is not None) and (e1 <= s2):
            return False
        if (e2 is not None) and (s1 is not None) and e2 <= s1:
            return False
        return True

    @classmethod
    def intersect2(cls, span1, span2):
        if (not span1) or (not span2):
            return tuple([])

        if not cls.overlaps(span1, span2):
            return tuple([])

        s1, e1 = span1
        s2, e2 = span2

        is_not_none = lambda x: x is not None
        s = max([s1, s2], key=AbsoluteOrder.null2min)
        e = min([e1, e2], key=AbsoluteOrder.null2max)
        return s, e

    @classmethod
    def cap2(cls, *_, **__):
        return cls.intersect2(*_, **__)

    @classmethod
    def spans2cap(cls, spans):
        capN = FunctionTool.f_binary2f_nary(cls.cap2)
        return capN(spans)

    @classmethod
    def union(cls, span1, span2):
        if not cls.overlaps(span1, span2):
            return tuple([])

        s1, e1 = span1
        s2, e2 = span2

        s = min(s1, s2)
        e = max(e1, e2)
        return s, e

    @classmethod
    def cup(cls, *_, **__):
        return cls.union(*_, **__)

    @classmethod
    def overlaps_any(cls, span_list):
        span_list_sorted = sorted(span_list)
        n = len(span_list_sorted)

        if n <= 1:
            return False

        for i in range(n - 1):
            if cls.overlaps(span_list[i], span_list[i + 1]):
                return True
        return False

    @classmethod
    def span2is_valid(cls, span):
        s, e = span
        return s <= e

    @classmethod
    def span2none_if_invalid(cls, span):
        s, e = span
        if s > e:
            return None
        return span

    @classmethod
    def add_each(cls, span, v):
        return tmap(lambda x: x + v, span)

    @classmethod
    def covers_index(cls, span, index):
        if index is None:
            return False

        s, e = span

        return s <= index < e

    @classmethod
    def covers(cls, span1, span2):
        s1, e1 = span1
        s2, e2 = span2

        return s1 <= s2 and e1 >= e2

    @classmethod
    def equals(cls, span1, span2):
        s1, e1 = span1
        s2, e2 = span2

        return s1 == s2 and e1 == e2

    @classmethod
    def covers_strictly(cls, span1, span2):
        return cls.covers(span1, span2) and (not cls.equals(span1, span2))

    @classmethod
    def is_covered_by(cls, span1, span2):
        return cls.covers(span2, span1)


    @classmethod
    def span_list2indexes_uncovered(cls, span_list_in) -> Set[int]:

        span_list = lmap(tuple, span_list_in)
        n = len(span_list)

        h_duplicate = merge_dicts([{span: [i]} for i, span in enumerate(span_list)],
                                  vwrite=DictTool.VWrite.extend)

        i_list_sorted_start = sorted(range(n), key=lambda i: (span_list[i][0], -span_list[i][1]), )
        i_list_sorted_end = sorted(range(n), key=lambda i: (-span_list[i][1], span_list[i][0]), )

        h_i2i_set_hyp_start = {i: set(i_list_sorted_start[:j])
                               for j, i in enumerate(i_list_sorted_start)}
        h_i2i_set_hyp_end = {i: set(i_list_sorted_end[:j])
                             for j, i in enumerate(i_list_sorted_end)}

        i_set_uncovered_raw = sfilter(lambda i: not (h_i2i_set_hyp_start[i] & h_i2i_set_hyp_end[i]), range(n))

        index_set_uncovered = set(index
                                  for i in i_set_uncovered_raw
                                  for index in h_duplicate[span_list[i]])

        return index_set_uncovered


    @classmethod
    def index_iter2span_iter(cls, index_iter):
        start, end = None, None

        for i in index_iter:
            if start is None:
                start = end = i
                continue

            if i == end+1:
                end = i
                continue

            yield (start, end+1)

            start = end = i

        if start is not None:
            yield (start, end+1)

    @classmethod
    @IterTool.f_iter2f_list
    def index_list_exclusive2span_iter(cls, index_list_exclusive, n):
        start, end = 0, 0

        for i in index_list_exclusive:
            if i>end:
                yield (end, i)

            end = i+1

        if n > end:
            yield (end,n)



    @classmethod
    def obj_list2uncovered(cls, obj_list, f_obj2span=None):
        if f_obj2span is None:
            f_obj2span = lambda x:x

        span_list = lmap(f_obj2span, obj_list)
        i_set_uncovered = cls.span_list2indexes_uncovered(span_list)
        return lmap(lambda i:obj_list[i], i_set_uncovered)

    @classmethod
    def list_spans_func2processed(cls, l_in, span_list, func, f_list2chain=None):
        if f_list2chain is None:
            f_list2chain = lambda ll:lchain(*ll)

        if not span_list:
            return l_in

        ll = []
        n = len(span_list)
        for i in range(n):
            s_this, e_this = span_list[i]
            e_prev = span_list[i - 1][1] if i > 0 else 0

            if s_this > e_prev:
                ll.append(l_in[e_prev:s_this])

            l_in_this = l_in[s_this:e_this]
            l_out_this = func(l_in_this)
            ll.append(l_out_this)

        e_last = span_list[-1][1]
        if e_last < len(l_in):
            ll.append(l_in[e_last:])

        l_out = f_list2chain(ll)
        return l_out

    @classmethod
    def span2len(cls, span, zero=0, inf=math.inf):
        if span is None:
            return None

        if not span:  # empty tuple means 0 length span
            return zero

        if (span[0] is None) or (span[1] is None):
            return inf

        return span[1] - span[0]


    @classmethod
    def _spans_index_limit2j_end_longest(cls, span_list, i, j_prev, len_limit):
        n = len(span_list)
        span_start = span_list[i]
        for j in range(j_prev, n):
            span_end = span_list[j]

            span_big = [span_start[0], span_end[1]]
            len_big = cls.span2len(span_big)

            if len_big <= len_limit: continue
            # if j-1 == j_prev: return None

            return j # last valid one
        return n

    @classmethod
    def span_list_limit2span_of_span_longest_iter(cls, span_list, len_limit):
        n = len(span_list)

        j_prev = 0
        for i in range(n):
            j_prev = max(i, j_prev)
            j_new = cls._spans_index_limit2j_end_longest(span_list, i, j_prev, len_limit, )
            if j_new == j_prev: continue

            yield (i, j_new)
            if j_new == n: break

            j_prev = j_new

    @classmethod
    def span_limit2extended(cls, span, limit):
        n = cls.span2len(span)
        buffer = max(limit - n, 0)

        s, e = span

        s_new = max(s - buffer//2, 0)
        e_new = e + buffer//2

        return (s_new, e_new)

    @classmethod
    def size2beam(cls, size):
        buffer_up = (size - 1) // 2
        buffer_down = (size - 1) // 2 + size % 2
        beam = (buffer_up, buffer_down)
        return beam

    @classmethod
    def values2bucket_indexes(
            cls,
            values_sorted: Iterable[T],
            pivots: List[T],
    ):
        def pivot2f_verifier(pivot):
            return lambda v: v < pivot
        f_verifiers = lmap(pivot2f_verifier, pivots)
        return IterTool.values2bucket_indexes(values_sorted, f_verifiers)
