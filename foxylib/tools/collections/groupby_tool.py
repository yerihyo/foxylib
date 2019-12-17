from collections import defaultdict

from functools import reduce
from operator import itemgetter as ig

from future.utils import lmap
from itertools import groupby
from nose.tools import assert_true

from foxylib.tools.collections.sort_tool import SortTool

class GroupbyToolkit:
    @classmethod
    def gb_tree_local(cls, objs, funcs,
                           leaf_func=lambda x: x,
                           ):
        if not funcs:
            l_objs = list(objs)
            return leaf_func(l_objs)
        return [(k, cls.gb_tree_local(v, funcs[1:], leaf_func=leaf_func))
                for k, v in groupby(objs, funcs[0])]


    @classmethod
    def gb_tree_global(cls, objs, funcs,
                            leaf_func=lambda l: l,
                            ):
        obj_list = list(objs)
        n_funcs = len(funcs)
        if not n_funcs: return leaf_func(obj_list)

        keys_obj_list = [tuple([func(obj) for func in funcs]) + (obj,)
                         for obj in obj_list]

        funcs_ig = [ig(i) for i in range(n_funcs)]
        keys_obj_list_sorted = reduce(lambda l, f_key: SortTool.sorted_by_key_index(l, f_key, ),
                                      reversed(funcs_ig),
                                      keys_obj_list,
                                      )
        gb_tree = cls.gb_tree_local(keys_obj_list_sorted,
                                     funcs_ig,
                                     leaf_func=lambda l: leaf_func(lmap(ig(n_funcs), l)),
                                     )
        return gb_tree

    @classmethod
    def h_gb_tree(cls, iter, funcs):
        l_in = list(iter)
        assert_true(funcs)

        f = funcs[0]
        h = defaultdict(list)

        for x in l_in:
            k = f(x)
            h[k].append(x)

        if len(funcs)==1:
            return h

        h_out = {k: cls.h_gb_tree(l, funcs[1:]) for k, l in h.items()}
        return h_out


GBToolkit = GroupbyToolkit
gb_tree_local = GBToolkit.gb_tree_local
gb_tree_global = GBToolkit.gb_tree_global
h_gb_tree = GBToolkit.h_gb_tree