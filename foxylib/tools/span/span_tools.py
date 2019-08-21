from future.utils import lmap, lfilter

from foxylib.tools.collections.collections_tools import lchain


class SpanToolkit:
    @classmethod
    def covers(cls, se1, se2):
        s1, e1 = se1
        s2, e2 = se2

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
    def str_span2substr(cls, str_in, span):
        s,e = span
        return str_in[s:e]

    @classmethod
    def span2len(cls, span): return max(span[1]-span[0],0)

str_span2substr = SpanToolkit.str_span2substr