import logging
from collections import defaultdict, OrderedDict
from dataclasses import dataclass

from functools import reduce, lru_cache
from operator import itemgetter as ig
from pprint import pformat, pprint
from typing import Iterable, TypeVar, Callable, List, Any, Dict, Set, cast, Generic

from future.utils import lmap
from itertools import groupby, chain
from nose.tools import assert_true, assert_equal

from foxylib.tools.collections.collections_tool import zip_strict, list2singleton, merge_dicts, vwrite_no_duplicate_key, \
    DictTool
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.collections.sort_tool import SortTool
from foxylib.tools.dataclass.dataclass_tool import DataclassTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

T = TypeVar("T")
Q = TypeVar("Q")

K = TypeVar("K")
V = TypeVar("V")


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

    # @classmethod
    # def groupby_tree_global_OLD(cls, objs, funcs,
    #                         leaf_func=lambda l: l,
    #                         ):
    #     obj_list = list(objs)
    #     n_funcs = len(funcs)
    #     if not n_funcs: return leaf_func(obj_list)
    #
    #     keys_obj_list = [tuple([func(obj) for func in funcs]) + (obj,)
    #                      for obj in obj_list]
    #
    #     funcs_ig = [ig(i) for i in range(n_funcs)]
    #     keys_obj_list_sorted = reduce(lambda l, f_key: SortTool.sorted_by_key_index(l, f_key, ),
    #                                   reversed(funcs_ig),
    #                                   keys_obj_list,
    #                                   )
    #     gb_tree = cls.groupby_tree_local(keys_obj_list_sorted,
    #                                      funcs_ig,
    #                                      leaf_func=lambda l: leaf_func(lmap(ig(n_funcs), l)),
    #                                  )
    #     return gb_tree

    @classmethod
    def iter2dicttree(cls, iter: Iterable[T], funcs: List[Callable[[T], Any]]):
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

        h_out = {k: cls.iter2dicttree(l, funcs[1:]) for k, l in h.items()}
        return h_out

    @classmethod
    def dicttree2reversed(
            cls,
            h_in: Dict[K, List[V]],
    ) -> Dict[V, Set[K]]:
        """
        Logic below will...
        First, create list of {string:{string}} dictionaries. (string=>set)
        Then, merge_dicts will merge this list of dictionaries into a single dictionary
        When there is conflict on keys, merge_dicts will union the values (DictToolkit.VWrite.union).
        """
        h_out = merge_dicts([
            {v: {k}}
            for k, v_list in h_in.items()
            for v in v_list],
            vwrite=DictTool.VWrite.union)

        return h_out

    @classmethod
    def tree2ordered_list(cls, tree_in, f_keys):
        if not f_keys:
            return tree_in

        keys = list(tree_in.keys())
        i_list_sorted = sorted(range(len(keys)), key=lambda i: f_keys[0](keys[i]))
        return [cls.tree2ordered_list(tree_in[keys[i]], f_keys[1:])
                for i in i_list_sorted]

    @classmethod
    def tree2aligned_list(cls, tree_in, pivot_lists):
        logger = FoxylibLogger.func_level2logger(cls.tree2aligned_list, logging.DEBUG)

        if not pivot_lists:
            return tree_in

        h_pivot2index = merge_dicts(
            [{k: i} for i, k in enumerate(pivot_lists[0])],
            vwrite=vwrite_no_duplicate_key)

        logger.debug(pformat({
            'tree_in': tree_in,
            'pivot_lists': pivot_lists,
        }))

        result = [[] for _ in range(len(h_pivot2index))]
        for k, v in tree_in.items():
            i = h_pivot2index[k]
            result[i] = cls.tree2aligned_list(v, pivot_lists[1:])
        return result

    @classmethod
    def groupby_tree_global_ordered(cls, objects, funcs, ordered_lists):
        h = cls.iter2dicttree(objects, funcs)
        return cls.tree2aligned_list(h, ordered_lists)

    @classmethod
    def objects2ordered_groups(cls, objects, f_key, ordered_keys):
        return cls.groupby_tree_global_ordered(objects, [f_key], [ordered_keys])


class DuplicateTool:
    @dataclass(frozen=True)
    class Info(Generic[K, T]):
        index: int
        key: K
        item: T

        @classmethod
        @lru_cache(maxsize=64)
        def fn2chkd(cls, fieldname):
            return DataclassTool.fieldname2checked(cls, fieldname)

        @classmethod
        def info2index(cls, info: 'DuplicateTool.Info[K,T]') -> int:
            return info.index if info else info

        @classmethod
        def info2key(cls, info: 'DuplicateTool.Info[K,T]') -> K:
            return info.key if info else info

        @classmethod
        def info2item(cls, info: 'DuplicateTool.Info[K,T]') -> T:
            return info.item if info else info

        @classmethod
        def iterable2infos(
                cls,
                iterable: Iterable[T],
                key: Callable[[T], K] = None,
        ) -> 'List[DuplicateTool.Info[K,T]]':
            key: K = key if key is not None else (lambda z: z)

            for i, x in enumerate(iterable):
                k = key(x)

                yield cls(index=i, key=k, item=x)

    @classmethod
    def iter2duplicate_infos(
            cls,
            iterable: Iterable[T],
            key: Callable[[T], K] = None,
    ) -> Iterable['DuplicateTool.Info']:
        """
        Basically identical to dict_group_by, but in iterable form to be able to return as soon as duplicate found
        """

        from foxylib.tools.collections.collections_tool import l_singleton2obj

        h_key2infos: Dict[str, List[DuplicateTool.Info]] = defaultdict(list)

        for info in cls.Info.iterable2infos(iterable, key=key):
            k: K = cls.Info.info2key(info)
            infos_prev: List[DuplicateTool.Info] = h_key2infos[k]

            # if not infos_prev:
            #     raise Exception({'info':info, 'h_key2infos':h_key2infos, 'infos_prev':infos_prev,})
            # duplicate found for the first time. yield previous duplicate
            if len(infos_prev) == 1:
                yield l_singleton2obj(infos_prev)

            # duplicate existed beforehand. yield me
            if infos_prev:
                yield info

            infos_prev.append(info)

    @classmethod
    def iter2dict_duplicates(
            cls,
            iterable: Iterable[T],
            key: Callable[[T], K] = None,
    ) -> Dict[K, List['DuplicateTool.Info[K, T]']]:
        duplicate_infos: Iterable[DuplicateTool.Info[K, T]] = list(cls.iter2duplicate_infos(iterable, key=key))
        dict_key2infos: Dict[K, List[DuplicateTool.Info[K, T]]] = GroupbyTool.iter2dicttree(
            duplicate_infos, [cls.Info.info2key], )
        return dict_key2infos


gb_tree_local = GroupbyTool.groupby_tree_local
gb_tree_global = GroupbyTool.groupby_tree_global
dict_groupby_tree = GroupbyTool.iter2dicttree