from collections import defaultdict

from functools import reduce
from operator import itemgetter as ig

from future.utils import lmap
from itertools import groupby, chain
from nose.tools import assert_true, assert_equal

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.collections.sort_tool import SortTool

class GroupbyTool:
    @classmethod
    def groupby_tree_local(cls, objs, funcs,
                           leaf_func=lambda x: x,
                           ):
        if not funcs:
            l_objs = list(objs)
            return leaf_func(l_objs)
        return [(k, cls.groupby_tree_local(v, funcs[1:], leaf_func=leaf_func))
                for k, v in groupby(objs, funcs[0])]

    @classmethod
    def groupby_tree_global(cls, objs, funcs, leaf_func=None,):
        if leaf_func is None:
            leaf_func = lambda l: l

        obj_list, func_list = list(objs), list(funcs)
        if not func_list:
            return leaf_func(obj_list)

        n, p = len(obj_list), len(func_list)  # index: i, j
        keys_obj_list = [tuple(chain([func(obj) for func in funcs], [obj]))
                         for obj in obj_list]

        dict_value2first_index_list = [IterTool.iter2dict_value2first_index(map(ig(j), keys_obj_list))
                                       for j in range(p)]

        def keys_obj2key_sort(keys_obj):
            assert_equal(len(keys_obj), p+1)
            keys, obj = keys_obj[:-1], keys_obj[-1]

            indexes = [dict_value2first_index_list[j][key] for j, key in enumerate(keys)]
            return tuple(chain(indexes, [obj]))

        funcs_ig = [ig(i) for i in range(p)]
        gb_tree = cls.groupby_tree_local(sorted(keys_obj_list, key=keys_obj2key_sort),
                                         funcs_ig,
                                         leaf_func=lambda l: leaf_func(lmap(ig(p), l)),
                                         )
        return gb_tree

    @classmethod
    def groupby_tree_global_OLD(cls, objs, funcs,
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
        gb_tree = cls.groupby_tree_local(keys_obj_list_sorted,
                                         funcs_ig,
                                         leaf_func=lambda l: leaf_func(lmap(ig(n_funcs), l)),
                                     )
        return gb_tree

    @classmethod
    def dict_groupby_tree(cls, iter, funcs):
        l_in = list(iter)
        assert_true(funcs)

        f = funcs[0]
        h = {}

        for x in l_in:
            k = f(x)
            if k not in h:
                h[k] = []
            h[k].append(x)

        if len(funcs) == 1:
            return h

        h_out = {k: cls.dict_groupby_tree(l, funcs[1:]) for k, l in h.items()}
        return h_out


gb_tree_local = GroupbyTool.groupby_tree_local
gb_tree_global = GroupbyTool.groupby_tree_global
dict_groupby_tree = GroupbyTool.dict_groupby_tree