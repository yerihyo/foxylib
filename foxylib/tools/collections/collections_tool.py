import logging
from functools import reduce, total_ordering, partial, wraps
from itertools import chain, product, zip_longest
from operator import itemgetter as ig
from typing import List

import numpy
from future.utils import lmap, lfilter
from nose.tools import assert_equal, assert_false, assert_true

from foxylib.tools.collections.iter_tool import IterTool, iter2singleton
from foxylib.tools.function.function_tool import funcs2piped, f_a2t
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.log.logger_tool import LoggerTool
from foxylib.tools.native.native_tool import is_none, is_not_none


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
    @IterTool.f_iter2f_list
    def list_pivotlist2aligned(cls, target_list, pivot_list, key=None):
        k_list = lmap(key, target_list) if key else target_list
        i_list = cls.list_pivotlist2indexes(k_list, pivot_list)

        for i in i_list:
            yield (target_list[i] if i is not None else None)




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
        from foxylib.tools.collections.groupby_tool import DuplicateTool
        h_key2duplicates = DuplicateTool.iter2dict_duplicates(l, key=key)
        if not h_key2duplicates:
            return

        raise cls(h_key2duplicates)


class ListTool:
    @classmethod
    def indexes2filtered(cls, l, indexes):
        return [l[i] for i in indexes]

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
    class Mode:
        ERROR_IF_DUPLICATE_KEY = 1
        ERROR_IF_KV_MISMATCH = 2
        OVERRIDE = 3

    class _LookupFailed(Exception):
        pass

    @classmethod
    def reversed(cls, h):
        return merge_dicts([{v: k} for k, v in h.items()],
                           vwrite=vwrite_no_duplicate_key)

    @classmethod
    def objects2dict(cls, objects, key):
        return merge_dicts([{key(x): x} for x in objects],
                           vwrite=vwrite_no_duplicate_key)

    # def lookup2cache_wrapper(cls, f_lookup):
    #     h = {}
    #
    #     def obj2cache(obj):
    #         return DictTool.get_or_init(h_obj2cache, obj, self2cache(obj))
    #
    #     return obj2cache

    @classmethod
    def filter_keys(cls, dict_in, keys):
        if not dict_in:
            return dict_in

        return cls.filter(lambda k, v: k in keys, dict_in)

    @classmethod
    def exclude_keys(cls, dict_in, keys):
        return cls.filter(lambda k, v: k not in keys, dict_in)

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
        if not h: return h
        return dict(filter(f_a2t(f_kv2is_valid), h.items()))

    @classmethod
    def kv2is_v_null(cls, kv):
        k, v = kv
        return v is None

    @classmethod
    def nullvalues2excluded(cls, h):
        return DictTool.filter(lambda kv: not cls.kv2is_v_null(kv), h),

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

                are_all_dicts = all([isinstance(v_h, dict),
                                     isinstance(v_in, dict),
                                     ])
                are_all_lists = all([isinstance(v_h, list),
                                     isinstance(v_in, list),
                                     ])
                if are_all_dicts:
                    v_out = merge_dicts([v_h, v_in], vwrite=f_hvwrite)
                    h_out = merge_dicts([h, {k: v_out}],
                                        vwrite=DictTool.VWrite.overwrite)
                elif are_all_lists:
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
        def update_if_identical(cls, h, k, v_in):
            if k not in h:
                return DictTool.update_n_return(h, k, v_in)

            v_prev = h[k]
            if v_prev == v_in:
                return h

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
            if (not h_from): # None
                return h_to

            if vwrite is None:
                vwrite = DictTool.VWrite.update_if_identical

            for k, v in h_from.items():
                h_to = vwrite(h_to, k, v)
            return h_to


        @classmethod
        def merge_dicts(cls, h_iter, vwrite=None,):
            h_list = list(filter(bool, h_iter))
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
        if x is None: return cls.MIN
        return x

    @classmethod
    def null2max(cls, x):
        if x is None: return cls.MAX
        return x

    @classmethod
    def true2min(cls, v):
        if bool(v): return cls.MIN
        return v

    @classmethod
    def true2max(cls, v):
        if bool(v): return cls.MAX
        return v

    @classmethod
    def false2min(cls, v):
        if not bool(v): return cls.MIN
        return v

    @classmethod
    def false2max(cls, v):
        if not bool(v): return cls.MAX
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
vwrite_update_if_identical = DictTool.VWrite.update_if_identical
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
llmap_batch = LLTool.llmap_batch

llmap = LLTool.llmap
llfilter = LLTool.llfilter
llchain = LLTool.llchain
ll_depths2lchained = LLTool.ll_depths2lchained
transpose = LLTool.transpose

bisect_by = IterTool.bisect_by
nsect_by = IterTool.nsect_by
