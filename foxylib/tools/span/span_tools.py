from future.utils import lmap, lfilter


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
