from collections import OrderedDict, Counter
from functools import reduce

from future.utils import lmap
from nose.tools import assert_equal, assert_false

from foxylib.tools.log.logger_tools import FoxylibLogger, LoggerToolkit
from foxylib.tools.native.function_tools import f_a2t
from foxylib.version import __version__

from foxylib.tools.native.builtin_tools import pipe_funcs, idfun, sfilter, is_none
from operator import itemgetter as ig

from foxylib.tools.version.version_tools import VersionToolkit


def l_singleton2obj(l, allow_empty_list=False):
    if len(l) == 1: return l[0]
    if not l and allow_empty_list: return None
    raise Exception(len(l), l)


s_singleton2obj = pipe_funcs([list, l_singleton2obj])





def iter2singleton(iterable, idfun=None, ):
    if idfun is None: idfun = lambda x: x

    it = iter(iterable)
    v = next(it)
    k = idfun(v)
    if not all(k == idfun(x) for x in it): raise Exception()
    return v

list2singleton = iter2singleton





class IterToolkit:
    @classmethod
    def classify_by(cls, iterable, func_list):
        l_all = list(iterable)
        result = tuple(map(lambda x: [], range(len(func_list) + 1)))

        for obj in l_all:
            index = next((i for i, func in enumerate(func_list) if func(obj)),
                         len(func_list),
                         )
            result[index].append(obj)

        if sum(lmap(len, result)) != len(l_all):
            raise Exception(" vs ".join([str(len(x)) for x in [l_all] + result]))

        return result

    @classmethod
    def iter2iList_duplicates(cls, iterable, key=None, ):
        from foxylib.tools.collections.itertools_tools import lchain

        if key is None:
            key = lambda x: x

        l_IN = list(iterable)
        h = OrderedDict()
        for i, x in enumerate(l_IN):
            k = key(x)
            h[k] = lchain(h.get(k,[]),[i])

        return lchain.from_iterable(filter(lambda l:len(l)>1, h.values()))

    @classmethod
    def iter2duplicate_list(cls, iterable, key=None,):
        l = list(iterable)
        iList = cls.iter2iList_duplicates(l, key=key)
        return lmap(lambda i:l[i], iList)

    @classmethod
    def uniq(cls, seq, idfun=None):
        seen = set()
        if idfun is None:
            for x in seq:
                if x in seen: continue
                seen.add(x)
                yield x
        else:
            for x in seq:
                y = idfun(x)
                if y in seen: continue
                seen.add(y)
                yield x

uniq = IterToolkit.uniq
iuniq = IterToolkit.uniq
luniq = pipe_funcs([IterToolkit.uniq, list])

class ListPairAlign:
    class Mode:
        PERFECT = "PERFECT"
        L1_COVERED = "L1_COVERED"
        L2_COVERED = "L2_COVERED"
        FREEFORM = "FREEFORM"

    @classmethod
    @LoggerToolkit.SEWrapper.info(func2logger=FoxylibLogger.func2logger)
    def list_pair2i2_list_aligned(cls, l1, l2,):
        logger = FoxylibLogger.func2logger(cls.list_pair2i2_list_aligned)
        h2 = merge_dicts([{x2:i2} for i2,x2 in enumerate(l2)],
                         vwrite=vwrite_no_duplicate_key)

        # logger.debug({"l1": l1,
        #               "l2": l2,
        #               "h2": h2,
        #               })

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



iter2duplicate_list = IterToolkit.iter2duplicate_list
lfilter_duplicate = IterToolkit.iter2duplicate_list


class DuplicateException(Exception):
    @classmethod
    def chk_n_raise(cls, l, key=None, ):
        duplicate_list = IterToolkit.iter2duplicate_list(l, key=key)
        if not duplicate_list: return

        raise cls(duplicate_list)

class ListToolkit:
    @classmethod
    def append_n_return(cls, l, v):
        l.append(v)
        return l

    @classmethod
    def ix_iter2x_list(cls, ix_iter):
        ix_list = list(ix_iter)

        assert_false(iter2duplicate_list(map(ig(0), ix_list)))

        n = len(ix_list)

        l = [None]*n
        for i,x in ix_list:
            l[i] = x
        return l




class DictToolkit:
    class Mode:
        ERROR_IF_DUPLICATE_KEY = 1
        ERROR_IF_KV_MISMATCH = 2
        OVERRIDE = 3

    class _LookupFailed(Exception):
        pass

    @classmethod
    def filter(cls, f_kv2is_valid, h):
        if not h: return h
        return dict(filter(f_a2t(f_kv2is_valid), h.items()))

    @classmethod
    def keys2exclude(cls, h, keys):
        return cls.filter(lambda x: x[0] not in set(keys), h)

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
            if v is not None: return v

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
        def f_iter(h_iter,*args,**kwargs):
            h_list = list(h_iter)
            if not h_list: return default

            h_final = reduce(lambda h1,h2: f_binary(h1,h2,*args,**kwargs), h_list[1:], h_list[0])
            return h_final
        return f_iter


    @classmethod
    def reverse(cls, h, vwrite=None,):
        h_list = [{v:k} for k,v in h.items()]
        return cls.Merge.merge_dicts(h_list, vwrite=vwrite)
    flip = reverse

    @classmethod
    def h_k2v(cls, h, k, default=None):
        if not h: return default
        if k not in h: return default
        return h[k]

    class DuplicateKeyException(Exception): pass

    class VWrite:
        @classmethod
        def f_vresolve2f_vwrite(cls, f_vresolve):
            # this cannot not update dictionary
            def f_vwrite(h, k, v_in):
                v = f_vresolve(h, k, v_in)
                return DictToolkit.update_n_return(h, k, v)

            return f_vwrite

        @classmethod
        def no_duplicate_key(cls, h, k, v_in):
            if k not in h:
                return DictToolkit.update_n_return(h, k, v_in)

            raise DictToolkit.DuplicateKeyException()

        @classmethod
        def update_if_identical(cls, h, k, v_in):
            if k not in h:
                return DictToolkit.update_n_return(h, k, v_in)

            v_prev = h[k]
            if v_prev == v_in:
                return h

            raise DictToolkit.DuplicateKeyException()

        @classmethod
        def k_list_append2vwrite(cls, k_list_append, vwrite_in):
            def vwrite_wrapped(h, k, v_in):
                if k in k_list_append:
                    l = ListToolkit.append_n_return(h.get(k, []), v_in)
                    return DictToolkit.update_n_return(h, k, l)

                return vwrite_in(h, k, v_in)

            return vwrite_wrapped


        @classmethod
        def overwrite(cls, h, k, v_in):
            return DictToolkit.update_n_return(h,k,v_in)


    class Merge:
        @classmethod
        def merge2dict(cls, h_to, h_from, vwrite=None,):
            if (not h_from): # None
                return h_to

            if vwrite is None:
                vwrite = DictToolkit.VWrite.update_if_identical

            for k, v in h_from.items():
                h_to = vwrite(h_to, k, v)
            return h_to


        @classmethod
        def merge_dicts(cls, h_iter, vwrite=None,):
            h_list = list(h_iter)
            if not h_list: return {}

            f_iter = DictToolkit.f_binary2f_iter(cls.merge2dict)
            return f_iter(h_iter, vwrite=vwrite)

        @classmethod
        def overwrite(cls, h, **kwargs):
            return cls.merge_dicts([h, kwargs], vwrite=DictToolkit.VWrite.overwrite)




    ## Deprecated

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def _branchname_list2lookup_h(cls, branchname_list, h, ):
        if not h: raise cls._LookupFailed()

        v = h
        for bn in branchname_list:
            if bn not in v: raise cls._LookupFailed()
            v = v[bn]

        return v

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def branchname_list2lookup_h_list_or_f_default(cls, branchname_list, h_list, f_default=None, ):
        if f_default is None: f_default = lambda: None

        for h in h_list:
            try:
                return cls._branchname_list2lookup_h(branchname_list, h)
            except cls._LookupFailed:
                continue

        return f_default()

    bn_list_h_list2v_or_f_else = VersionToolkit.deprecated(func=branchname_list2lookup_h_list_or_f_default,
                                                           version_current=__version__, version_tos="0.3")

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def branchname_list2lookup_h_list_or_default(cls, branchname_list, h_list, default=None, ):
        return cls.bn_list_h_list2v_or_f_else(branchname_list, h_list, f_default=lambda: default)

    bn_list_h_list2v_or_else = VersionToolkit.deprecated(func=branchname_list2lookup_h_list_or_default,
                                                         version_current=__version__, version_tos="0.3")

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def tree_height2cleaned(cls, h, height, ):
        if height <= 1: return h

        h_OUT = {}
        for k, v in h.items():
            if not v: continue

            v_OUT = cls.tree_height2cleaned(v, height - 1)
            if not v_OUT: continue

            h_OUT[k] = v_OUT

        return h_OUT

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def tree_func_list2reduced(cls, h, f_list):
        f = f_list[0]
        if len(f_list) <= 1:
            h_CHILD = h
        else:
            h_CHILD = {k: cls.tree_func_list2reduced(v, f_list[1:])
                       for k, v in h.items()}

        if f is None:
            h_OUT = h_CHILD
        else:
            h_OUT = f(h_CHILD)
        return h_OUT

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def tree_func_list2reduced_and_cleaned(cls, h, f_list):
        h_REDUCED = cls.tree_func_list2reduced(h, f_list)
        h_CLEANED = cls.tree_height2cleaned(h_REDUCED, len(f_list))
        return h_CLEANED

    tree_func_list2RnC = VersionToolkit.deprecated(func=tree_func_list2reduced_and_cleaned,
                                                   version_current=__version__, version_tos="0.3", )

    @classmethod
    @VersionToolkit.deprecated(version_current=__version__, version_tos="0.3")
    def depth_func_pairlist2f_list(cls, depth_func_pairlist):
        if not depth_func_pairlist: raise Exception()

        depth_list = lmap(ig(0), depth_func_pairlist)
        DuplicateException.chk_n_raise(depth_list)

        maxdepth = max(map(ig(0), depth_func_pairlist))
        l = [None, ] * (maxdepth + 1)

        for depth, func in depth_func_pairlist:
            l[depth] = func

        for i in range(len(l)):
            if l[i] is not None: continue
            l[i] = idfun

        return l


merge_dicts = DictToolkit.Merge.merge_dicts
overwrite = DictToolkit.Merge.overwrite

vwrite_no_duplicate_key = DictToolkit.VWrite.no_duplicate_key
vwrite_update_if_identical = DictToolkit.VWrite.update_if_identical
vwrite_overwrite = DictToolkit.VWrite.overwrite
