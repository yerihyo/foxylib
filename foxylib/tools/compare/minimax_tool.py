from future.utils import lmap
from nose.tools import assert_false, assert_is_none, assert_greater


class MinimaxTool:
    @classmethod
    def indexes_minimax(cls, l, cmp=None):
        if cmp is None:
            cmp = lambda a, b: -1 if a < b else (1 if a > b else 0)

        i_list_min = []
        i_list_max = []
        x0 = x1 = None

        for i, x in enumerate(l):
            if not i_list_min:
                assert_false(i_list_max)
                assert_is_none(x0)
                assert_is_none(x1)

                i_list_min = [i]
                i_list_max = [i]
                x0 = x1 = x
                continue

            cmp0 = cmp(x, x0)
            if cmp0 < 0:
                i_list_min = [i]
                x0 = x
            elif cmp0 == 0:
                i_list_min.append(i)

            cmp1 = cmp(x, x1)
            if cmp1 > 0:
                i_list_max = [i]
                x1 = x
            elif cmp0 == 0:
                i_list_max.append(i)

        return i_list_min, i_list_max

    @classmethod
    def indexes_minimax_n(cls, l, p):
        assert_greater(p, 0)

        n = len(l)
        i_list_sorted = sorted(range(n), key=lambda i:l[i])


        j_min = next(filter(lambda j: l[j] != l[j - 1], range(p, n)), n)
        j_max = next(filter(lambda j: l[j] != l[j + 1], reversed(range(n-p))), 0)

        # raise Exception({"n":n,
        #                  "p":p,
        #                  "j_min":j_min,
        #                  "j_max":j_max,
        #                  "i_list_sorted":i_list_sorted,
        #                  "l":l,
        #                  })

        indexes_min = i_list_sorted[:j_min]
        indexes_max = i_list_sorted[j_max:]

        return (indexes_min, indexes_max)

    @classmethod
    def indexes_min_n(cls, l, p):
        return cls.indexes_minimax_n(l, p)[0]

    @classmethod
    def indexes_max_n(cls, l, p):
        return cls.indexes_minimax_n(l, p)[1]


    @classmethod
    def minimaxes_n(cls, l, p, key=None):
        if key is None:
            key = lambda x:x

        k_list = lmap(key, l)
        indexes_min, indexes_max = cls.indexes_minimax_n(k_list,p,)

        mins = lmap(lambda i: l[i], indexes_min)
        maxs = lmap(lambda i: l[i], indexes_max)

        return (mins,maxs)

    @classmethod
    def min_n(cls, l, p, key=None,):
        return cls.minimaxes_n(l, p, key=key)[0]

    @classmethod
    def max_n(cls, l, p, key=None,):
        return cls.minimaxes_n(l, p, key=key)[1]

    @classmethod
    def minimax(cls, iter, key=None):
        x0, x1 = None, None
        k0, k1 = None, None

        if key is None:
            key = lambda x: x

        for x in iter:
            k = key(x)
            if x0 is None or k < k0:
                x0, k0 = x, k

            if x1 is None or k > k1:
                x1, k1 = x, k
        return x0, x1

    @classmethod
    def max_or_default(cls, l, default):
        if not l:
            return default
        return max(l)

minimax = MinimaxTool.minimax

max_or_default = MinimaxTool.max_or_default