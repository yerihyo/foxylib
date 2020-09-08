from collections import defaultdict, OrderedDict

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
        if not obj_list:
            return []

        if not func_list:
            return leaf_func(obj_list)

        n, p = len(obj_list), len(func_list)  # index: i, j
        keys_index_obj_list = [tuple(chain([func(obj) for func in funcs], [i, obj]))
                         for i, obj in enumerate(obj_list)]

        dict_value2first_index_list = [IterTool.iter2dict_value2first_index(map(ig(j), keys_index_obj_list))
                                       for j in range(p)]

        def keys_index_obj2key_sort(keys_index_obj_list):
            assert_equal(len(keys_index_obj_list), p+2)
            keys, i = keys_index_obj_list[:-2], keys_index_obj_list[-2]

            indexes = [dict_value2first_index_list[j][key] for j, key in enumerate(keys)]
            return tuple(chain(indexes, [i]))

        funcs_ig = [ig(i) for i in range(p)]
        gb_tree = cls.groupby_tree_local(sorted(keys_index_obj_list, key=keys_index_obj2key_sort),
                                         funcs_ig,
                                         leaf_func=lambda l: leaf_func(lmap(ig(p+1), l)),
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
        # l_in = list(iter)
        assert_true(funcs)

        f = funcs[0]
        h = {}

        for x in iter:
            k = f(x)
            if k not in h:
                h[k] = [x]
            else:
                h[k].append(x)

        if len(funcs) == 1:
            return h

        h_out = {k: cls.dict_groupby_tree(l, funcs[1:]) for k, l in h.items()}
        return h_out


class DuplicateTool:
    class Doc:
        class Field:
            INDEX = "index"
            KEY = "key"
            ITEM = "item"

        @classmethod
        def doc2index(cls, doc):
            return doc[cls.Field.INDEX]

        @classmethod
        def doc2key(cls, doc):
            return doc[cls.Field.KEY]

        @classmethod
        def doc2item(cls, doc):
            return doc[cls.Field.ITEM]

        @classmethod
        def iterable2docs(cls, iterable, key=None,):
            key = key if key is not None else (lambda z: z)

            for i, x in enumerate(iterable):
                k = key(x)

                yield {cls.Field.INDEX: i,
                       cls.Field.KEY: k,
                       cls.Field.ITEM: x,
                       }

    @classmethod
    def iter2duplicate_docs(cls, iterable, key=None, ):
        """
        Basically identical to dict_group_by, but in iterable form to be able to return as soon as duplicate found
        """

        from foxylib.tools.collections.collections_tool import l_singleton2obj

        h_key2docs = defaultdict(list)

        for doc in cls.Doc.iterable2docs(iterable, key=key):
            k = cls.Doc.doc2key(doc)
            docs_prev = h_key2docs.get(k)

            # duplicate found for the first time. yield previous duplicate
            if len(docs_prev) == 1:
                yield l_singleton2obj(docs_prev)

            # duplicate existed beforehand. yield me
            if docs_prev:
                yield doc

            docs_prev.append(doc)

    @classmethod
    def iter2dict_duplicates(cls, iterable, key=None, ):
        return GroupbyTool.dict_groupby_tree(cls.iter2duplicate_docs(iterable, key=key), [cls.Doc.doc2key],)


gb_tree_local = GroupbyTool.groupby_tree_local
gb_tree_global = GroupbyTool.groupby_tree_global
dict_groupby_tree = GroupbyTool.dict_groupby_tree