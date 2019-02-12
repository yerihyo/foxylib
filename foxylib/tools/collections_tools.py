from collections import OrderedDict

from future.utils import lmap

from foxylib.tools.builtin_tools import pipe_funcs


def l_singleton2obj(l, allow_empty_list=False):
    if len(l) == 1: return l[0]
    if not l and allow_empty_list: return None
    raise Exception(len(l), l)


s_singleton2obj = pipe_funcs([list, l_singleton2obj])


def uniq_iterable(seq, idfun=None):
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


iuniq = uniq_iterable
luniq = pipe_funcs([uniq_iterable, list])


def iter2singleton(iterable, idfun=None, ):
    if idfun is None: idfun = lambda x: x

    it = iter(iterable)
    v = next(it)
    k = idfun(v)
    if not all(k == idfun(x) for x in it): raise Exception()
    return v

list2singleton = iter2singleton


def lfilter_duplicate(iterable, key=None):
    if key is None: key = lambda x: x

    l_IN = list(iterable)
    h = OrderedDict()
    for i, x in enumerate(l_IN):
        k = key(x)
        if k not in h: h[k] = []
        h[k].append(i)

    l_OUT = [l_IN[i]
             for k, iList in h.items()
             if len(iList) > 1
             for i in iList]
    return l_OUT

class DuplicateException(Exception):
    @classmethod
    def chk_n_raise(cls, l, key=None, ):
        l_DUPLICATE = lfilter_duplicate(l, key=key)
        if not l_DUPLICATE: return

        raise cls(l_DUPLICATE)

class DictToolkit:
    class _LookupFailed(Exception):
        pass

    @classmethod
    def h2vs(cls, h):
        if not h: return h
        return list(h.values())

    @classmethod
    def _branchname_list2lookup_h(cls, branchname_list, h, ):
        if not h: raise cls._LookupFailed()

        v = h
        for bn in branchname_list:
            if bn not in v: raise cls._LookupFailed()
            v = v[bn]

        return v

    @classmethod
    def branchname_list2lookup_h_list_or_f_default(cls, branchname_list, h_list, f_default=None, ):
        if f_default is None: f_default = lambda: None

        for h in h_list:
            try:
                return cls._branchname_list2lookup_h(branchname_list, h)
            except cls._LookupFailed:
                continue

        return f_default()

    bn_list_h_list2v_or_f_else = branchname_list2lookup_h_list_or_f_default

    @classmethod
    def branchname_list2lookup_h_list_or_default(cls, branchname_list, h_list, default=None, ):
        return cls.bn_list_h_list2v_or_f_else(branchname_list, h_list, f_default=lambda: default)

    bn_list_h_list2v_or_else = branchname_list2lookup_h_list_or_default

    @classmethod
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
    def tree_func_list2reduced_and_cleaned(cls, h, f_list):
        h_REDUCED = cls.tree_func_list2reduced(h, f_list)
        h_CLEANED = cls.tree_height2cleaned(h_REDUCED, len(f_list))
        return h_CLEANED

    tree_func_list2RnC = tree_func_list2reduced_and_cleaned

    @classmethod
    def depth_func_pairlist2f_list(cls, depth_func_pairlist):
        if not depth_func_pairlist: raise Exception()

        depth_list = lmap(ig(0), depth_func_pairlist)
        DuplicateException.chk_n_raise(depth_list)

        maxdepth = max(imap(ig(0), depth_func_pairlist))
        l = [None, ] * (maxdepth + 1)

        for depth, func in depth_func_pairlist:
            l[depth] = func

        for i in xrange(len(l)):
            if l[i] is not None: continue
            l[i] = idfun

        return l
