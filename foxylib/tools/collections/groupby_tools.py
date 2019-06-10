from functools import reduce
from operator import itemgetter as ig

from future.utils import lmap
from itertools import groupby

from foxylib.tools.collections.sort_tools import SortToolkit

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
        keys_obj_list_sorted = reduce(lambda l, f_key: SortToolkit.sorted_by_key_index(l, f_key, ),
                                      reversed(funcs_ig),
                                      keys_obj_list,
                                      )
        gb_tree = cls.gb_tree_local(keys_obj_list_sorted,
                                     funcs_ig,
                                     leaf_func=lambda l: leaf_func(lmap(ig(n_funcs), l)),
                                     )
        return gb_tree


GBToolkit = GroupbyToolkit
gb_tree_local = GBToolkit.gb_tree_local
gb_tree_global = GBToolkit.gb_tree_global