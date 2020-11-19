from collections import defaultdict
from typing import Set, Tuple, List

from foxylib.tools.number.number_tool import NumberTool, SignTool
from future.utils import lmap, lfilter
from nose.tools import assert_greater_equal, assert_less_equal

from foxylib.tools.collections.iter_tool import IterTool, iter2singleton
from foxylib.tools.collections.collections_tool import lchain, tmap, merge_dicts, \
    DictTool, sfilter
from foxylib.tools.span.span_tool import SpanTool


class IndexspanTool:
    @classmethod
    def steps(cls, start, end):
        step = SignTool.sign(end - start)
        yield from SpanTool.steps(start, end, step)

    @classmethod
    def span2is_valid(cls, span):
        if not span:
            return False

        s, e = span

        if s * e == 0:
            if s == 0 and e == 0:
                return True

            return s == 0

        elif s * e > 0:
            return s <= e

        else:
            return s > 0

    @classmethod
    def list_span2is_valid(cls, l, span):
        if l is None:
            return False

        if not cls.span2is_valid(span):
            return False

        n = len(l)
        s, e = span
        if s-e > n:
            return False

        if s > n:
            return False

        if -e > n:
            return False

        return True

    @classmethod
    def list_span2sublist(cls, l, span):
        if not cls.list_span2is_valid(l, span):
            return None

        s, e = span
        return l[s:e]

    @classmethod
    def index_total_beam2span(cls, index, total, beam):
        buffer_pre, buffer_post = beam

        count_return = sum(beam) + 1
        if index <= buffer_pre:
            return (0, min(count_return, total),)

        if index + buffer_post >= total - 1:
            return (max(0, total - buffer_post), total)

        return (index - buffer_pre, index + buffer_post + 1)

    @classmethod
    def index_values_beam2neighbor_indexes(cls, i_pivot, v_list, beam):
        v_count = len(v_list)
        i_list_sorted = sorted(range(v_count), key=lambda i: v_list[i])
        k_pivot = iter2singleton(
            filter(lambda k: i_list_sorted[k] == i_pivot, range(v_count)))
        k_span = cls.index_total_beam2span(k_pivot, v_count, beam)

        i_sublist = cls.list_span2sublist(i_list_sorted, k_span)
        return i_sublist

    @classmethod
    def span_list_span2span_big(cls, span_list, span_of_span):
        span_list_partial = cls.list_span2sublist(span_list, span_of_span)
        return [span_list_partial[0][0], span_list_partial[-1][1]]

    @classmethod
    def span_iter2merged(cls, span_iter):
        span_list_in = lfilter(bool, span_iter)  # se might be None
        if not span_list_in: return []

        l_sorted = sorted(map(list, span_list_in))
        n = len(l_sorted)

        l_out = []
        ispan_start = 0
        iobj_end = l_sorted[0][-1]
        for ispan in range(n - 1):
            s2, e2 = l_sorted[ispan + 1]

            if iobj_end >= s2:
                iobj_end = max(iobj_end, e2)
                continue

            span_out = cls.span_list_span2span_big(l_sorted,
                                                   (ispan_start, ispan + 1))
            l_out.append(span_out)
            ispan_start = ispan + 1

        span_last = cls.span_list_span2span_big(l_sorted, (ispan_start, n))
        l_out.append(span_last)

        return l_out

    @classmethod
    def span2iter(cls, span):
        return range(*span)


list_span2sublist = IndexspanTool.list_span2sublist
# span2iter = IndexspanTool.span2iter