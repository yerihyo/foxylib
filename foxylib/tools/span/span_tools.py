from future.utils import lmap, lfilter

from foxylib.tools.collections.collections_tools import lchain, iter2singleton, IterToolkit, f_iter2f_list


class SpanToolkit:
    @classmethod
    def span2iter(cls, span):
        return range(*span)

    @classmethod
    def span_size2is_valid(cls, span, n):
        s,e = span
        return s>=0 and e<=n and s<=e

    @classmethod
    def span_size2valid(cls, span, n):
        s, e = span
        return (max(0,s),min(e,n))

    @classmethod
    def add_each(cls, span, v):
        return tuple(IterToolkit.add_each(span, v))

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
    def is_covered_by(cls, se1, se2):
        return cls.covers(se2,se1)

    @classmethod
    def find_root(cls, h_parent, index):
        i = index
        while True:
            if i not in h_parent:
                return i
            i = h_parent[i]

    @classmethod
    def se_indices2se_covering(cls, se_in, indices):
        s_in, e_in = se_in
        s = None
        for i in indices:
            if i >= e_in:
                return (s,i) if s is not None else None

            if i <= s_in:
                s = i
        return None


    @classmethod
    def se_list2h_parent(cls, se_list):
        n = len(se_list)
        ilist_sorted = sorted(range(n), key=lambda i: se_list[i])

        h_parent = {}

        for i in range(1,n):
            i_this = ilist_sorted[i]
            if i_this in h_parent:
                continue

            se_this = se_list[i_this]
            i_prev = cls.find_root(h_parent, ilist_sorted[i-1])
            se_prev = se_list[i_prev]
            if cls.is_covered_by(se_this, se_prev):
                h_parent[i_this] = i_prev
            if cls.covers(se_this, se_prev):
                h_parent[i_prev] = i_this

        return h_parent

    @classmethod
    def se_list2index_list_covered(cls, se_list):
        h_parent = cls.se_list2h_parent(se_list)
        return list(h_parent.keys())

    @classmethod
    def se_list2index_list_uncovered(cls, se_list):
        n = len(se_list)
        ilist_covered = cls.se_list2index_list_covered(se_list)
        ilist_uncovered = lfilter(lambda i:i not in ilist_covered, range(n))
        return ilist_uncovered

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
    @f_iter2f_list
    def index_list_exclusive2span_iter(cls, index_list_exclusive, n):
        start, end = 0, 0

        for i in index_list_exclusive:
            if i>end:
                yield (end, i)

            end = i+1

        if n > end:
            yield (end,n)



    @classmethod
    def obj_list2uncovered(cls, obj_list, f_obj2se=None):
        if f_obj2se is None:
            f_obj2se = lambda x:x

        se_list = lmap(f_obj2se, obj_list)
        ilist_uncovered = cls.se_list2index_list_uncovered(se_list)
        return lmap(lambda i:obj_list[i], ilist_uncovered)

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
    def list_span2sublist(cls, str_in, span):
        s,e = span
        return str_in[s:e]

    @classmethod
    def span2len(cls, span): return max(span[1]-span[0],0)


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

            span_out = cls.span_list_span2span_big(l_sorted, (ispan_start, ispan+1))
            l_out.append(span_out)
            ispan_start = ispan + 1

        span_last = cls.span_list_span2span_big(l_sorted, (ispan_start, n))
        l_out.append(span_last)

        return l_out

    @classmethod
    def size2beam(cls, size):
        buffer_up = (size - 1) // 2
        buffer_down = (size - 1) // 2 + size % 2
        beam = (buffer_up, buffer_down)
        return beam

    @classmethod
    def index_total_beam2span(cls, index, total, beam):
        buffer_pre, buffer_post = beam

        count_return = sum(beam)+1
        if index <= buffer_pre:
            return (0, min(count_return,total),)

        if index + buffer_post >= total-1:
            return (max(0,total-buffer_post),total)

        return (index-buffer_pre,index+buffer_post+1)

    @classmethod
    def index_values_beam2neighbor_indexes(cls, i_pivot, v_list, beam):
        v_count = len(v_list)
        i_list_sorted = sorted(range(v_count), key=lambda i:v_list[i])
        k_pivot = iter2singleton(filter(lambda k: i_list_sorted[k] == i_pivot, range(v_count)))
        k_span = cls.index_total_beam2span(k_pivot, v_count, beam)

        i_sublist = cls.list_span2sublist(i_list_sorted, k_span)
        return i_sublist




list_span2sublist = SpanToolkit.list_span2sublist
span2iter = SpanToolkit.span2iter