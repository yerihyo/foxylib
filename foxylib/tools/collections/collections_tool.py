import logging
from dataclasses import dataclass
from functools import reduce, total_ordering, partial, wraps
from itertools import chain, product, groupby
from operator import itemgetter as ig
from pprint import pformat
from typing import List, TypeVar, Tuple, Iterable, Dict, Callable, Optional, Any, Set

import numpy
from future.utils import lmap, lfilter
from nose.tools import assert_equal, assert_false, assert_true

from foxylib.tools.collections.iter_tool import IterTool, iter2singleton
from foxylib.tools.function.function_tool import funcs2piped, f_a2t
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.log.logger_tool import LoggerTool
from foxylib.tools.native.native_tool import is_none, is_not_none

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class IterWrapper:
    @classmethod
    def iter2list(cls, func=None):
        def wrapper(f):
            @wraps(f)
            def wrapped(*_, **__):
                iter = f(*_,**__)
                return list(iter)

            return wrapped

        return wrapper(func) if func else wrapper


class ListPairAlign:
    class Mode:
        PERFECT = "PERFECT"
        L1_COVERED = "L1_COVERED"
        L2_COVERED = "L2_COVERED"
        FREEFORM = "FREEFORM"

    @classmethod
    def list_pivotlist2indexes(cls, target_list, pivot_list, ):
        n = len(pivot_list)
        h = merge_dicts([{pivot_list[i]: i} for i in range(n)],
                        vwrite=vwrite_no_duplicate_key)

        return [h.get(x) for x in target_list]

    @classmethod
    def list_pivotlist2aligned(cls, target_list, pivot_list, key=None):
        k_list = lmap(key, target_list) if key else target_list
        i_list = cls.list_pivotlist2indexes(k_list, pivot_list)

        return [target_list[i] if i is not None else None
                for i in i_list]

    @classmethod
    @LoggerTool.SEWrapper.info(func2logger=partial(FoxylibLogger.func_level2logger, level=logging.DEBUG))
    def list_pair2i2_list_aligned(cls, l1, l2,):
        h2 = merge_dicts([{x2:i2} for i2,x2 in enumerate(l2)],
                         vwrite=vwrite_no_duplicate_key)
        return [h2.get(x1) for x1 in l1]

    @classmethod
    def _mode_n1_i2_list2check(cls, mode, n1, i2_list):
        set_l1_uncovered = set(range(n1)) - set(i2_list)
        set_i2_uncovered = sfilter(is_none, i2_list)

        if mode == cls.Mode.FREEFORM:
            return

        if mode == cls.Mode.PERFECT:
            assert_equal(n1, len(i2_list))
            assert_false(set_l1_uncovered)
            assert_false(set_i2_uncovered)
            return

        if mode == cls.Mode.L1_COVERED:
            assert_false(set_l1_uncovered)
            return

        if mode == cls.Mode.L2_COVERED:
            assert_false(set_i2_uncovered)
            return

        raise Exception()

    @classmethod
    def list_pair2l2_aligned(cls, l1, l2, mode, default=None,):
        i2_list = cls.list_pair2i2_list_aligned(l1,l2)
        cls._mode_n1_i2_list2check(mode, len(l1), i2_list,)

        l2_aligned = [l2[i2] if i2 is not None else default
                      for i2 in i2_list]
        return l2_aligned


class DuplicateException(Exception):
    @classmethod
    def chk_n_raise(cls, l, key=None, ):
        if not l:
            return

        from foxylib.tools.collections.groupby_tool import DuplicateTool
        h_key2duplicates = DuplicateTool.iter2dict_duplicates(l, key=key)
        if not h_key2duplicates:
            return

        raise cls(h_key2duplicates)


@dataclass(frozen=True)
class Rankdata:
    rankindex: int
    rank: int
    tiecount: int
    value: any

    @classmethod
    def values2rankdata_list(cls, values) -> List['Rankdata']:
        from foxylib.tools.collections.groupby_tool import GroupbyTool

        n = len(values)

        value2indexes_list = GroupbyTool.groupby_tree_local(range(n), [lambda i: values[i]])

        def value_indexes2rankdata(value, indexes):
            rankindex = min(indexes)

            rankdata = Rankdata(rankindex=rankindex, rank=rankindex+1, tiecount=len(indexes), value=value)
            return rankdata

        return [value_indexes2rankdata(value, indexes)
                for value, indexes in value2indexes_list]

    @classmethod
    def values2dict_value2rankdata(cls, values) -> Dict[Any, 'Rankdata']:
        rankdata_list = cls.values2rankdata_list(values)

        return merge_dicts([{rankdata.value: rankdata} for rankdata in rankdata_list],
                    vwrite=DictTool.VWrite.no_duplicate_key)


class ListTool:
    @classmethod
    def innerproduct(cls, l1, l2):
        n = IterTool.iter2singleton([len(l1), len(l2)])
        return sum([l1[i] * l2[i] for i in range(n)])

    @classmethod
    def uniq(cls, iterable: Iterable[T]) -> List[T]:
        return list(IterTool.uniq(iterable))

    @classmethod
    def splice(cls, l: List[T], span: Tuple[int, int], sub: List[T]) -> List[T]:
        b = l[:span[0]]
        e = l[span[1]:]
        return lchain(b, sub, e)

    @classmethod
    def indexes2filtered(cls, l: List[T], indexes: Iterable[int]) -> List[T]:
        return [l[i] for i in indexes]

    @classmethod
    def lookup(cls, l, i, default=None):
        return l[i] if len(l) > i else default

    @classmethod
    def transpose(cls, ll):
        return map(list, zip(*ll))

    @classmethod
    def transpose_strict(cls, ll):
        return map(list, IterTool.zip_strict(*ll))

    @classmethod
    def index2sub(cls, array_in, index, value):
        array_out = lchain(array_in[:index], [value], array_in[index+1:])
        return array_out

    @classmethod
    def is_sorted(cls, list_in, key=None):
        if key is None:
            key = lambda x:x

        n = len(list_in)
        for i in range(1, n):
            if key(list_in[i-1]) > key(list_in[i]):  # i is the index of the previous element
                return False

        return True

    @classmethod
    def f_batch2f_batch_bijected(cls, f_batch, indexes_bijection):
        # x_list => y_list
        # z_list => w_list
        def f_batch_bijected(x_list, *_, **__):
            n = len(x_list)

            dict_i2j = {i: j for j, i in enumerate(indexes_bijection)}

            z_list = [x_list[i] for i in indexes_bijection]
            w_list = f_batch(z_list, *_, **__)
            assert_equal(len(z_list), len(w_list))

            y_list = [w_list[dict_i2j[i]] for i in range(n)]
            return y_list
        return f_batch_bijected

    @classmethod
    def f_batch2bijected(cls, f_batch, indexes_bijection, x_list, *_, **__):
        f_batch_bijected = cls.f_batch2f_batch_bijected(f_batch, indexes_bijection)
        return f_batch_bijected(x_list, *_, **__)

    @classmethod
    def list2indexes_maiden(
            cls,
            items: List[T],
            items_existing: Optional[Set[T]] = None,
    ):
        logger = FoxylibLogger.func_level2logger(cls.list2indexes_maiden, logging.DEBUG)

        n = len(items)
        indexes_uniq = luniq(range(n), lambda i: items[i])
        indexes_maiden = lfilter(lambda i: items[i] not in items_existing, indexes_uniq) if items_existing else indexes_uniq

        # logger.debug({
        #     'len(items)': len(items),
        #     'len(indexes_uniq)': len(indexes_uniq),
        #     'len(indexes_maiden)': len(indexes_maiden),
        #     'len(items_existing)': len(items_existing),
        # })

        return indexes_maiden

    @classmethod
    def _mapreduce(cls, objs_in, obj2index, f_objs2results_list, mapreducetype:str):
        logger = FoxylibLogger.func_level2logger(cls.mapreduce, logging.DEBUG)

        obj_list_in = list(objs_in)
        n, m = len(obj_list_in), len(f_objs2results_list)

        h_j2indexes = merge_dicts(
            [{obj2index(obj): [i]} for i, obj in enumerate(obj_list_in)],
            vwrite=DictTool.VWrite.extend)

        obj_list_out = [None for _ in range(n)]
        for j in range(m):
            indexes = h_j2indexes.get(j)
            if not indexes:
                continue

            f_objs2results = f_objs2results_list[j]

            page_out = f_objs2results(lmap(lambda i: obj_list_in[i], indexes))
            # if len(page_out) != len(indexes):
            #     logger.debug(pformat({
            #         'len(page_out)': len(page_out),
            #         'len(indexes)': len(indexes),
            #         'page_out':page_out,
            #         'indexes':indexes,
            #     }))
            if mapreducetype != 'mapreduce':
                continue

            # logger.debug({'page_out':page_out, 'indexes':indexes})

            p = list2singleton([len(page_out), len(indexes)])

            for k in range(p):
                obj_list_out[indexes[k]] = page_out[k]

        return obj_list_out if mapreducetype == 'mapreduce' else None

    @classmethod
    def mapreduce(cls, objs_in, obj2index, f_objs2results_list):
        return cls._mapreduce(objs_in, obj2index, f_objs2results_list, 'mapreduce')

    @classmethod
    def mapbatch(cls, objs_in, obj2index, f_objs2results_list):
        cls._mapreduce(objs_in, obj2index, f_objs2results_list, 'mapbatch')

    # @classmethod
    # def sub_or_append(cls, array1, array2, key=None):
    #     if key is None:
    #         key = lambda x: x
    #
    #     n1 = len(array1)
    #     keys1 = lmap(key, array1)
    #     h1_k2i = DictTool.objects2dict(range(n1), key=lambda i1: keys1[i1])
    #
    #     n2 = len(array2)
    #     keys2 = lmap(key, array2)
    #     h2_k2i = DictTool.objects2dict(range(n2), key=lambda i2: keys2[i2])
    #
    #     keys_all = luniq(chain(keys1,keys2))
    #
    #     def key2value(k):
    #         if k in h2_k2i:
    #             i2 = h2_k2i[k]
    #             v2 = array2[i2]
    #             return v2
    #
    #         i1 = h1_k2i[k]
    #         v1 = array1[i1]
    #         return v1
    #
    #     values = lmap(key2value, keys_all)
    #     return values

    @classmethod
    def sub_or_append(cls, arrays, key=None):
        if key is None:
            key = lambda x: x

        n = len(arrays)
        p_list = lmap(len, arrays)
        h_k2j_list = [
            DictTool.objects2dict(range(p_list[i]),
                                  key=lambda j: key(arrays[i][j]))
            for i in range(n)]

        keys_all = luniq(chain(*map(lambda h: h.keys(), h_k2j_list)))

        def key2value(k):
            for i in reversed(range(n)):
                h_k2j = h_k2j_list[i]
                if k in h_k2j:
                    j = h_k2j[k]
                    v = arrays[i][j]
                    return v
            raise NotImplementedError("Should not come here!!")

        values = lmap(key2value, keys_all)
        return values




    @classmethod
    @IterTool.f_iter2f_list
    def list_detector2span_list(cls, x_list, f_detector):
        i_start = 0
        n = len(x_list)

        for i, x in enumerate(x_list):
            if not f_detector(x_list, i):
                continue

            yield (i_start, i)
            i_start = i

        yield (i_start, n)

    @classmethod
    def table2col_count(cls, ll):
        return iter2singleton(map(len, ll))

    @classmethod
    def lappend(cls, l, v):
        l.append(v)
        return l

    @classmethod
    def ix_iter2x_list(cls, ix_iter):
        from foxylib.tools.collections.groupby_tool import DuplicateTool
        ix_list = list(ix_iter)

        assert_true(IterTool.iter2is_empty(DuplicateTool.iter2duplicate_docs(map(ig(0), ix_list))))

        n = len(ix_list)

        l = [None]*n
        for i, x in ix_list:
            l[i] = x
        return l

    @classmethod
    @IterWrapper.iter2list
    def value2front(cls, l, v):
        n = len(l)
        i_list_matching = lfilter(lambda i:l[i]==v, range(n))
        yield from map(lambda i:l[i], i_list_matching)

        i_set_matching = set(i_list_matching)
        yield from map(lambda i:l[i], filter(lambda i:i not in i_set_matching, range(n)))


    @classmethod
    def li2v(cls, l, i): return l[i]

    @classmethod
    def l_singleton2obj(cls, iterable, allow_empty_list=False):
        l = list(iterable)
        if len(l) == 1:
            return l[0]

        if not l and allow_empty_list:
            return None

        raise Exception(len(l), l)

    @classmethod
    def objs_filters2objs_valid_first(cls, l_in, f_list):
        for f in f_list:
            l_valid = lfilter(f, l_in)
            if l_valid: return l_valid

        return None

    @classmethod
    def list2tuple(cls, v):
        if not isinstance(v, list):
            return v

        return tuple(v)

    @classmethod
    def chain_each(cls, *xs_ll):
        l = []
        for xs_list in IterTool.zip_strict(*xs_ll):
            x_list = lchain(*xs_list)
            l.append(x_list)
        return l

    @classmethod
    def intersperse(cls, l, delim):
        result = [delim] * (len(l) * 2 - 1)
        result[0::2] = l
        return result

    # @classmethod
    # def list_buffer2func(cls, l, limit, func):
    #     if len(l) < limit:
    #         return l
    #
    #     func(l)
    #     return []

    @classmethod
    def iv_lists2merged(cls, iv_lists):
        h_list = [{i: v}
             for iv_list in iv_lists
             for i, v in iv_list]

        h = merge_dicts(h_list, vwrite=vwrite_no_duplicate_key)
        n = len(h)

        assert_false(set(range(n)) - set(h.keys()))

        l_out = [h[i] for i in range(n)]
        return l_out

    @classmethod
    def ll_indexes2lookup(cls, ll_in, index_list):
        return [ll_in[j][index] for j,index in enumerate(index_list)]


class DictTool:
    class Operation:
        INSERT = 'INSERT'
        REPLACE = 'REPLACE'
        UPDATE = 'UPDATE'
        # UPSERT = 'UPSERT'

    class _LookupFailed(Exception):
        pass

    @classmethod
    def get(cls, h:dict, k):
        return h.get(k) if h else None

    @classmethod
    def reversed(cls, h):
        return merge_dicts([{v: k} for k, v in h.items()],
                           vwrite=vwrite_no_duplicate_key)

    @classmethod
    def objects2dict(
            cls,
            objects: Iterable[T],
            key: Callable[[T], K],
            value: Callable[[T], V] = None,
    ) -> Dict[K, V]:
        if value is None:
            value = lambda v: v

        return merge_dicts([{key(x): value(x)} for x in objects],
                           vwrite=vwrite_no_duplicate_key)

    @classmethod
    def dict2values_mapped(
            cls,
            h_in: Dict[K, List[V]],
            f_map: Callable[[V], T],
    ) -> Dict[K, List[T]]:
        logger = FoxylibLogger.func_level2logger(cls.dict2values_mapped, logging.DEBUG)
        if not f_map:
            return h_in
        # logger.debug({"dict_value2texts":dict_value2texts})

        h_out = {k: lmap(f_map, v_list)
                for k, v_list in h_in.items()}
        return h_out

    @classmethod
    def keys2remapped(cls, dict_in, dict_map):
        return {dict_map.get(k,k): v for k, v in dict_in.items()}

    @classmethod
    def filter_keys(cls, dict_in, keys):
        if not dict_in:
            return dict_in

        return cls.filter(lambda k, v: k in keys, dict_in)

    @classmethod
    def exclude_keys(cls, dict_in, keys):
        return cls.filter(lambda k, v: k not in keys, dict_in)

    @classmethod
    def keys_excluded(cls, dict_in, keys):
        return cls.exclude_keys(dict_in, keys)

    @classmethod
    def lazyget(cls, dict_in, key, f_default=None):
        def v():
            if f_default is not None:
                return f_default()
            return None

        if dict_in is None:
            return v()

        if key not in dict_in:
            dict_in[key] = v()

        return dict_in[key]

    @classmethod
    def append_key2values(cls, h):
        return {k: lchain(vs, [k])
                for k, vs in h.items()}

    @classmethod
    def get_or_lazyinit(cls, h, k, f_v):
        if k not in h:
            h[k] = f_v()

        return h[k]

    @classmethod
    def get_or_init(cls, h, k, v):
        return cls.get_or_lazyinit(h, k, lambda: v)

    @classmethod
    def pop(cls, h, k, default=None):
        if not h:
            return default

        return h.pop(k, default)

    @classmethod
    def dicts2keys(cls, dicts):
        return set.union(*[set(h.keys()) for h in dicts])


    @classmethod
    def filter(cls, f_kv2is_valid, h):
        if not h:
            return h
        return dict(filter(f_a2t(f_kv2is_valid), h.items()))

    # @classmethod
    # def kv2is_v_null(cls, kv):
    #     k, v = kv
    #     return v is None

    @classmethod
    def nullvalues2excluded(cls, h):
        return DictTool.filter(lambda k,v: v is not None, h)

    @classmethod
    def invalidvalues2excluded(cls, h, f_valid):
        return DictTool.filter(lambda k, v: f_valid(v), h)

    @classmethod
    def emptyvalues2excluded(cls, h):
        def is_emptyvalue(x):
            if x is None:
                return True

            if bool(x):
                return False

            if isinstance(x, (list, tuple, dict)):
                return True

            return False

        return cls.invalidvalues2excluded(h, lambda v: not is_emptyvalue(v))

    @classmethod
    def falsevalues2excluded(cls, h):
        return DictTool.filter(lambda k, v: bool(v), h)

    @classmethod
    def keys2filtered(cls, h, keys):
        return cls.filter(lambda k,v: k in set(keys), h)

    @classmethod
    def keys2excluded(cls, h, keys):
        return cls.filter(lambda k,v: k not in set(keys), h)

    @classmethod
    def h2set_attrs(cls, obj, h):
        if not h: return obj

        for k, v in h.items():
            setattr(obj, k, v)

        return obj

    @classmethod
    def keys2v_first_or_default(cls, h, key_iter, default=None,):
        for k in key_iter:
            v = h.get(k)
            if v is not None:
                return v

        return default

    @classmethod
    def h2v_list(cls, h):
        if not h: return None
        return list(h.values())

    @classmethod
    def update_n_return(cls, h, k, v):
        h[k] = v
        return h

    @classmethod
    def f_binary2f_iter(cls, f_binary, default=None):
        def f_iter(h_iter, *_, **__):
            h_list_valid = lfilter(bool, h_iter)
            if not h_list_valid:
                return default

            h_final = reduce(lambda h1, h2: f_binary(h1, h2, *_, **__), h_list_valid, {})
            return h_final

        return f_iter



    @classmethod
    def flip(cls, h, vwrite=None,):
        h_list = [{v:k} for k,v in h.items()]
        return cls.Merge.merge_dicts(h_list, vwrite=vwrite)

    @classmethod
    def lookup(cls, h, k, default=None):
        if not h:
            return default
        if k not in h:
            return default
        return h[k]

    class DuplicateKeyException(Exception): pass

    class VResolve:
        @classmethod
        def extend(cls,h,k,v_in):
            v_this = h.get(k)
            if not v_this: return list(v_in)
            return lchain(list(v_in),list(v_this))

        @classmethod
        def union(cls, h, k, v_in):
            v_this = h.get(k)
            if not v_this: return set(v_in)
            return set.union(set(v_in), set(v_this))

    class VWrite:
        @classmethod
        def union(cls, h, k, v_in):
            h[k] = h.get(k, set([])) | set(v_in)
            return h

        @classmethod
        def f_vresolve2f_vwrite(cls, f_vresolve):
            # this cannot not update dictionary
            def f_vwrite(h, k, v_in):
                v = f_vresolve(h, k, v_in)
                return DictTool.update_n_return(h, k, v)

            return f_vwrite

        @classmethod
        def f_vwrite2f_hvwrite(cls, f_vwrite):
            def f_hvwrite(h, k, v_in):
                v_h = h.get(k)

                are_all_dicts = all([v_h is None or isinstance(v_h, dict),
                                     isinstance(v_in, dict),
                                     ])
                if are_all_dicts:
                    v_out = merge_dicts([v_h, v_in], vwrite=f_hvwrite)
                    h_out = merge_dicts([h, {k: v_out}],
                                        vwrite=DictTool.VWrite.overwrite)
                else:
                    h_out = f_vwrite(h, k, v_in)

                return h_out

            return f_hvwrite

        @classmethod
        def f_vwrite2f_hlvwrite(cls, f_vwrite):
            def f_hvwrite(h, k, v_in):
                v_h = h.get(k)

                are_all_dicts = all([v_h is None or isinstance(v_h, dict),
                                     isinstance(v_in, dict),
                                     ])
                are_all_lists = all([v_h is None or isinstance(v_h, list),
                                     isinstance(v_in, list),
                                     ])
                if are_all_dicts:
                    v_out = merge_dicts([v_h, v_in], vwrite=f_hvwrite)
                    h_out = merge_dicts([h, {k: v_out}],
                                        vwrite=DictTool.VWrite.overwrite)
                elif are_all_lists:
                    if v_h is None:
                        h_out = {k: v_in}
                    else:
                        # assert_equal(len(v_h), len(v_in))
                        n = list2singleton([len(v_h), len(v_in)])
                        # n_min = min([len(v_h), len(v_in)])

                        v_out = [merge_dicts([v_h[i], v_in[i]], vwrite=f_hvwrite)
                                 for i in range(n)]
                        h_out = merge_dicts([h, {k: v_out}],
                                            vwrite=DictTool.VWrite.overwrite)
                else:
                    h_out = f_vwrite(h, k, v_in)

                return h_out

            return f_hvwrite

        @classmethod
        def no_duplicate_key(cls, h, k, v_in):
            if k not in h:
                return DictTool.update_n_return(h, k, v_in)

            raise DictTool.DuplicateKeyException({"key":k})

        @classmethod
        def skip_if_existing(cls, h, k, v_in):
            if k in h:
                return h

            return DictTool.update_n_return(h, k, v_in)

        @classmethod
        def skip_if_identical(cls, h, k, v_in):
            if k not in h:
                return DictTool.update_n_return(h, k, v_in)

            v_prev = h[k]
            if v_prev == v_in:
                return h

            logger = FoxylibLogger.func_level2logger(cls.skip_if_identical, logging.DEBUG)
            logger.exception(pformat({'k':k, 'h':h, 'v_in': v_in}))
            raise DictTool.DuplicateKeyException()

        @classmethod
        def k_list_append2vwrite(cls, k_list_append, vwrite_in):
            def vwrite_wrapped(h, k, v_in):
                if k in k_list_append:
                    l = ListTool.lappend(h.get(k, []), v_in)
                    return DictTool.update_n_return(h, k, l)

                return vwrite_in(h, k, v_in)

            return vwrite_wrapped

        @classmethod
        def extend(cls, h, k, l_in):
            l_out = lchain(h.get(k, []), l_in)
            return DictTool.update_n_return(h, k, l_out)

        @classmethod
        def overwrite(cls, h, k, v_in):
            return DictTool.update_n_return(h,k,v_in)


    class Merge:
        @classmethod
        def merge2dict(cls, h_to, h_from, vwrite=None,):
            if (not h_from):  # None
                return h_to

            if vwrite is None:
                vwrite = DictTool.VWrite.skip_if_identical

            for k, v in h_from.items():
                h_to = vwrite(h_to, k, v)
            return h_to


        @classmethod
        def merge_dicts(cls, h_iter, vwrite=None,):
            h_list = list(filter(bool, h_iter))
            # pprint(h_list)
            # raise Exception()
            if not h_list:
                return {}

            f_iter = DictTool.f_binary2f_iter(cls.merge2dict)
            return f_iter(h_list, vwrite=vwrite)

        @classmethod
        def overwrite(cls, h_iter,):
            return cls.merge_dicts(list(h_iter), vwrite=DictTool.VWrite.overwrite)





class SingletonTool:
    class NotSingletonError(Exception):
        @classmethod
        def chk_n_raise(cls, obj_list: List,):
            if not obj_list:
                raise cls()

            if len(obj_list) != 1:
                raise cls()

            return ListTool.l_singleton2obj(obj_list)

    class NoObjectError(Exception):
        @classmethod
        def chk_n_raise(cls, obj_list,):
            if obj_list: return obj_list

            raise cls()

    class TooManyObjectsError(Exception):
        @classmethod
        def chk_n_raise(cls, obj_list, limit):
            if not obj_list:
                return obj_list

            if len(obj_list) <= limit:
                return obj_list

            raise cls()


class LLTool:
    @classmethod
    def _ll2flat_dim(cls, ll, count_unwrap):
        if count_unwrap < 0:
            raise Exception()

        if count_unwrap == 0:
            return ll, len(ll)

        flat_dim_list = [cls._ll2flat_dim(l, count_unwrap - 1) for l in ll]
        (flat_ll, dim) = lmap(list, IterTool.zip_strict(*flat_dim_list))

        flat_list = lchain(*flat_ll)

        return flat_list, dim

    @classmethod
    def ll2flat(cls, ll, count_unwrap):
        flat_list, dim = cls._ll2flat_dim(ll, count_unwrap)
        return flat_list

    @classmethod
    def _flat_dim2ll_count(cls, flat_list, dim):
        if not isinstance(dim, list):
            return flat_list[:dim], dim

        ll = []
        i_flat = 0
        for d in dim:
            l, flat_len = cls._flat_dim2ll_count(flat_list[i_flat:], d)
            i_flat += flat_len
            ll.append(l)

        return ll, i_flat

    @classmethod
    def dim2flat_len(cls, dim):
        if isinstance(dim, int):
            return dim

        if isinstance(dim, (list, tuple,)): 
            return sum(lmap(cls.dim2flat_len, dim))

        raise NotImplementedError("No other type possible")

    @classmethod
    def flat_dim2ll(cls, flat_list, dim):
        ll, flat_len = cls._flat_dim2ll_count(flat_list, dim)
        assert_equal(cls.dim2flat_len(dim), flat_len)

        return ll

    @classmethod
    def ll2count_unwrap(cls, ll):

        if not isinstance(ll, list):
            return 0

        l = IterTool.filter2first(is_not_none, ll)
        return cls.ll2count_unwrap(l)+1

    @classmethod
    def f_batch2f_n_ll(cls, f_batch,):
        @wraps(f_batch)
        def f_wrapped(count_unwrap, ll, *args, **kwargs):
            if count_unwrap == 0: return f_batch(ll, *args, **kwargs)

            flat_list, dim = cls._ll2flat_dim(ll, count_unwrap)
            n_input = len(flat_list)

            v_list = f_batch(flat_list, *args, **kwargs)
            n_output = len(v_list)

            assert_equal(n_input, n_output,
                         "f_list() should neither remove elements nor modify order of elements!")

            v_ll, flat_len = cls._flat_dim2ll_count(v_list, dim, )
            return v_ll

        return f_wrapped

    @classmethod
    def f_batch_n2f_ll(cls, f_batch, count_unwrap):
        f_unwrap_ll = cls.f_batch2f_n_ll(f_batch)
        f_ll = partial(f_unwrap_ll, count_unwrap)
        return f_ll

    @classmethod
    def llmap_batch(cls, f_batch, ll, count_unwrap):
        f_ll = cls.f_batch_n2f_ll(f_batch, count_unwrap)
        v_ll = f_ll(ll)
        return v_ll

    @classmethod
    def llmap(cls, f, x, count_unwrap=1):
        if count_unwrap == 0:
            return f(x)

        return [cls.llmap(f, y, count_unwrap-1,) for y in x]

    @classmethod
    def llfilter(cls, f, ll, count_unwrap=0):
        if count_unwrap == 0:
            return lfilter(f, ll)

        return [cls.llfilter(f, y, count_unwrap - 1, ) for y in ll]

    @classmethod
    def llchain(cls, ll, count_unwrap=1):
        return reduce(lambda l, f: f(*l), [lchain] * count_unwrap, ll)

    @classmethod
    def f2f_args_permuted(cls, f, ll):
        if not ll:
            return f

        @wraps(f)
        def f_wrapped(*a, **k):
            l_out = []
            for x in ll[0]:
                f_x = cls.f2f_args_permuted(partial(f, x), ll[1:])
                v_x = f_x(*a, **k)

                l_out.append(v_x)
            return l_out

        return f_wrapped

    @classmethod
    def ll_depths2lchained(cls, ll, depths):
        if not depths:
            return ll

        depths_children = smap(lambda x:x-1, filter(bool, depths))
        ll_children = [cls.ll_depths2lchained(x, depths_children) for x in ll]

        return lchain(*ll_children) if 0 in depths else ll_children


    @classmethod
    def transpose(cls, ll, axes):
        return numpy.transpose(ll, axes).tolist()


class CollectionTool:
    @classmethod
    def func2traversing(cls, f):
        def f_recursive(x):
            if isinstance(x, (list, set, tuple,), ):
                return type(x)([f_recursive(v) for v in x])

            if isinstance(x, (dict,), ):
                return type(x)({k: f_recursive(v) for k, v in x.items()})

            return f(x)
        return f_recursive


class AbsoluteOrder:
    @total_ordering
    class _AbsoluteMin(object):
        def __eq__(self, other): return self is other

        def __le__(self, other): return True

    MIN = _AbsoluteMin()

    @total_ordering
    class _AbsoluteMax(object):
        def __eq__(self, other): return self is other

        def __ge__(self, other): return True

    MAX = _AbsoluteMax()

    @classmethod
    def null2min(cls, x):
        if x is None:
            return cls.MIN
        return x

    @classmethod
    def null2max(cls, x):
        if x is None:
            return cls.MAX
        return x

    @classmethod
    def true2min(cls, v):
        if bool(v):
            return cls.MIN
        return v

    @classmethod
    def true2max(cls, v):
        if bool(v):
            return cls.MAX
        return v

    @classmethod
    def false2min(cls, v):
        if not bool(v):
            return cls.MIN
        return v

    @classmethod
    def false2max(cls, v):
        if not bool(v):
            return cls.MAX
        return v


list2singleton = IterTool.iter2singleton

luniq = funcs2piped([IterTool.uniq, list])

sfilter = funcs2piped([filter, set])

l_singleton2obj = ListTool.l_singleton2obj
iter_singleton2obj = funcs2piped([list, ListTool.l_singleton2obj])

li2v = ListTool.li2v

hfilter = DictTool.filter

merge_dicts = DictTool.Merge.merge_dicts
dicts_overwrite = DictTool.Merge.overwrite

vwrite_no_duplicate_key = DictTool.VWrite.no_duplicate_key
vwrite_skip_if_identical = DictTool.VWrite.skip_if_identical
vwrite_overwrite = DictTool.VWrite.overwrite

f_vwrite2f_hvwrite = DictTool.VWrite.f_vwrite2f_hvwrite

lappend = ListTool.lappend
list2tuple = ListTool.list2tuple

chain_each = ListTool.chain_each
intersperse = ListTool.intersperse


ichain = chain
lchain = funcs2piped([chain, list])
tchain = funcs2piped([chain, tuple])
schain = funcs2piped([chain, set])

lreversed = funcs2piped([reversed, list])

luniqchain = funcs2piped([chain, IterTool.uniq, list])

lchain.from_iterable = funcs2piped([chain.from_iterable, list])

tmap = funcs2piped([map, tuple])
smap = funcs2piped([map, set])
lmap_singleton = funcs2piped([lmap, l_singleton2obj])

lproduct = funcs2piped([product,list])

zip_strict = IterTool.zip_strict
lzip_strict = funcs2piped([zip_strict, list])

map_strict = IterTool.map_strict
lmap_strict = funcs2piped([map_strict, list])


# LLTool
f_batch_n2f_ll = LLTool.f_batch_n2f_ll
# llmap_batch = LLTool.llmap_batch

llmap = LLTool.llmap
llfilter = LLTool.llfilter
llchain = LLTool.llchain
ll_depths2lchained = LLTool.ll_depths2lchained
transpose = LLTool.transpose

bisect_by = IterTool.bisect_by
nsect_by = IterTool.nsect_by

