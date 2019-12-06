import collections
import operator
import random
from collections import OrderedDict, deque
from functools import reduce, total_ordering, partial, wraps
from operator import itemgetter as ig

import numpy
from future.utils import lmap, lfilter
from itertools import chain, product, combinations, islice, count, groupby, repeat, starmap, tee, zip_longest, cycle, \
    filterfalse
from nose.tools import assert_equal, assert_false, assert_is_not_none, assert_is_none

from foxylib.tools.function.function_tools import funcs2piped, f_a2t, FunctionToolkit
from foxylib.tools.log.logger_tools import FoxylibLogger, LoggerToolkit
from foxylib.tools.native.native_tools import is_none, is_not_none
from foxylib.tools.nose.nose_tools import assert_all_same_length
from foxylib.tools.version.version_tools import VersionToolkit
from foxylib.version import __version__


class IterToolkit:


    @classmethod
    def add_each(cls, iter, v):
        for x in iter:
            yield x+v

    @classmethod
    def iter2chunks(cls, *_, **__):
        from foxylib.tools.collections.chunk_tools import ChunkToolkit
        yield from ChunkToolkit.chunk_size2chunks(*_, **__)

    @classmethod
    def list_func_count2index_list_continuous_valid(cls, l, f_valid, count_match):
        n = len(l)

        i_list_valid = lfilter(lambda i: all(f_valid(l[i + j]) for j in range(count_match)),
                               range(n-(count_match-1)))
        return i_list_valid

    @classmethod
    def iter2buffered(cls, iter, buffer_size):
        logger = FoxylibLogger.func2logger(cls.iter2buffered)

        if not buffer_size:
            yield from iter

        else:
            l = deque()
            for x in iter:
                l.append(x)

                # logger.debug({"len(l)":len(l), "buffer_size":buffer_size,})
                while len(l) > buffer_size:
                    yield l.popleft()

            while l:
                yield l.popleft()

    @classmethod
    def f_batch2f_iter(cls, f_batch, chunk_size):
        from foxylib.tools.collections.chunk_tools import ChunkToolkit

        def f_iter(iter, *_, **__):
            for x_list in ChunkToolkit.chunk_size2chunks(iter, chunk_size):
                y_list = f_batch(x_list, *_, **__)
                yield from y_list

        return f_iter

    @classmethod
    def iter_func2suffixed(cls, iter, f):
        for x in iter:
            yield (x,f(x))

    @classmethod
    def iter_func2prefixed(cls, iter, f):
        for x in iter:
            yield (f(x), x)


    @classmethod
    def iter2last(cls, iterable):
        i_cur,v = None, None
        for i, x in enumerate(iterable):
            i_cur = i
            v = x

        assert_is_not_none(i_cur)
        return v

    @classmethod
    def is_empty(cls, iter):
        for _ in iter:
            return False
        return True

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
    def _iter2singleton(cls, iterable, idfun=None, empty2null=True):
        if idfun is None: idfun = lambda x: x

        it = iter(iterable)
        try:
            v = next(it)
        except StopIteration:
            if empty2null: return None
            raise


        k = idfun(v)
        if not all(k == idfun(x) for x in it):
            raise Exception()
        return v

    @classmethod
    def iter2singleton(cls, iterable, idfun=None,):
        return cls._iter2singleton(iterable, idfun=idfun, empty2null=False)

    @classmethod
    def iter2singleton_or_none(cls, iterable, idfun=None, ):
        return cls._iter2singleton(iterable, idfun=idfun, empty2null=True)

    @classmethod
    def filter2first(cls, f, iterable, default=None):
        for x in filter(f, iterable):
            return x
        return default

    @classmethod
    def filter2singleton(cls, f, iterable):
        return cls.iter2singleton(filter(f, iterable))

    @classmethod
    def map2singleton(cls, f, iterable):
        return cls.iter2singleton(map(f, iterable))

    @classmethod
    def filter2single_or_none(cls, f, iterable):
        return cls.iter2singleton_or_none(filter(f, iterable))

    @classmethod
    def iter2iList_duplicates(cls, iterable, key=None, ):
        if key is None:
            key = lambda x: x

        l_IN = list(iterable)
        h = OrderedDict()
        for i, x in enumerate(l_IN):
            k = key(x)
            h[k] = lchain(h.get(k,[]),[i])

        return list(chain.from_iterable(filter(lambda l:len(l)>1, h.values())))

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

    @classmethod
    def zip_strict(cls, *list_of_list):
        assert_all_same_length(*list_of_list)
        return zip(*list_of_list)

    @classmethod
    def map_strict(cls, f, *list_of_list):
        assert_all_same_length(*list_of_list)
        return map(f, *list_of_list)



    @classmethod
    def lslice(cls, iter, n):
        return list(islice(iter,n))

    @classmethod
    def f_iter2f_list(cls, f_iter):
        def f_list(*_, **__):
            return list(f_iter(*_,**__))
        return f_list

    @classmethod
    def count(cls, iterable):
        return sum(1 for _ in iterable)




    @classmethod
    def nsect_by(cls, iterable, func_list):
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
    def bisect_by(cls, iterable, func):
        return cls.nsect_by(iterable, [func])

    @classmethod
    def first(cls, iterable):
        l = cls.head(1,iterable)
        if not l:
            return None
        return l[0]


    # from https://docs.python.org/3/library/itertools.html#itertools-recipes
    @classmethod
    def head(cls, n, iterable):
        return cls.take(n,iterable)

    @classmethod
    def take(cls, n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, n))

    @classmethod
    def prepend(cls, value, iterator):
        "Prepend a single value in front of an iterator"
        # prepend(1, [2, 3, 4]) -> 1 2 3 4
        return chain([value], iterator)

    @classmethod
    def tabulate(cls, function, start=0):
        "Return function(0), function(1), ..."
        return map(function, count(start))

    @classmethod
    def tail(cls, n, iterable):
        "Return an iterator over the last n items"
        # tail(3, 'ABCDEFG') --> E F G
        return iter(collections.deque(iterable, maxlen=n))

    @classmethod
    def consume(cls, iterator, n=None):
        "Advance the iterator n-steps ahead. If n is None, consume entirely."
        # Use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length deque
            collections.deque(iterator, maxlen=0)
        else:
            # advance to the empty slice starting at position n
            next(islice(iterator, n, n), None)

    @classmethod
    def nth(cls, iterable, n, default=None):
        "Returns the nth item or a default value"
        return next(islice(iterable, n, None), default)

    @classmethod
    def all_equal(cls, iterable):
        "Returns True if all the elements are equal to each other"
        g = groupby(iterable)
        return next(g, True) and not next(g, False)

    @classmethod
    def quantify(cls, iterable, pred=bool):
        "Count how many times the predicate is true"
        return sum(map(pred, iterable))

    @classmethod
    def padnone(cls, iterable):
        """Returns the sequence elements and then returns None indefinitely.

        Useful for emulating the behavior of the built-in map() function.
        """
        return chain(iterable, repeat(None))

    @classmethod
    def ncycles(cls, iterable, n):
        "Returns the sequence elements n times"
        return chain.from_iterable(repeat(tuple(iterable), n))

    @classmethod
    def dotproduct(cls, vec1, vec2, sum=sum, map=map, mul=operator.mul):
        return sum(map(mul, vec1, vec2))

    @classmethod
    def flatten(cls, listOfLists):
        "Flatten one level of nesting"
        return chain.from_iterable(listOfLists)

    @classmethod
    def repeatfunc(cls, func, times=None, *args):
        """Repeat calls to func with specified arguments.

        Example:  repeatfunc(random.random)
        """
        if times is None:
            return starmap(func, repeat(args))
        return starmap(func, repeat(args, times))

    @classmethod
    def pairwise(cls, iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    @classmethod
    def grouper(cls, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    @classmethod
    def roundrobin(cls, *iterables):
        "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
        # Recipe credited to George Sakkis
        num_active = len(iterables)
        nexts = cycle(iter(it).__next__ for it in iterables)
        while num_active:
            try:
                for next in nexts:
                    yield next()
            except StopIteration:
                # Remove the iterator we just exhausted from the cycle.
                num_active -= 1
                nexts = cycle(islice(nexts, num_active))

    @classmethod
    def partition(cls, pred, iterable):
        'Use a predicate to partition entries into false entries and true entries'
        # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
        t1, t2 = tee(iterable)
        return filterfalse(pred, t1), filter(pred, t2)

    @classmethod
    def powerset(cls, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    @classmethod
    def unique_everseen(cls, iterable, key=None):
        "List unique elements, preserving order. Remember all elements ever seen."
        # unique_everseen('AAAABBBCCDAABBB') --> A B C D
        # unique_everseen('ABBCcAD', str.lower) --> A B C D
        seen = set()
        seen_add = seen.add
        if key is None:
            for element in filterfalse(seen.__contains__, iterable):
                seen_add(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add(k)
                    yield element

    @classmethod
    def unique_justseen(cls, iterable, key=None):
        "List unique elements, preserving order. Remember only the element just seen."
        # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
        # unique_justseen('ABBCcAD', str.lower) --> A B C A D
        return map(next, map(ig(1), groupby(iterable, key)))

    @classmethod
    def iter_except(cls, func, exception, first=None):
        """ Call a function repeatedly until an exception is raised.

        Converts a call-until-exception interface to an iterator interface.
        Like builtins.iter(func, sentinel) but uses an exception instead
        of a sentinel to end the loop.

        Examples:
            iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
            iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
            iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
            iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
            iter_except(s.pop, KeyError)                             # non-blocking set iterator

        """
        try:
            if first is not None:
                yield first()  # For database APIs needing an initial cast to db.first()
            while True:
                yield func()
        except exception:
            pass

    @classmethod
    def first_true(cls, iterable, default=False, pred=None):
        """Returns the first true value in the iterable.

        If no true value is found, returns *default*

        If *pred* is not None, returns the first item
        for which pred(item) is true.

        """
        # first_true([a,b,c], x) --> a or b or c or x
        # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
        return next(filter(pred, iterable), default)

    @classmethod
    def random_product(cls, *args, repeat=1):
        "Random selection from itertools.product(*args, **kwds)"
        pools = [tuple(pool) for pool in args] * repeat
        return tuple(random.choice(pool) for pool in pools)

    @classmethod
    def random_permutation(cls, iterable, r=None):
        "Random selection from itertools.permutations(iterable, r)"
        pool = tuple(iterable)
        r = len(pool) if r is None else r
        return tuple(random.sample(pool, r))

    @classmethod
    def random_combination(cls, iterable, r):
        "Random selection from itertools.combinations(iterable, r)"
        pool = tuple(iterable)
        n = len(pool)
        indices = sorted(random.sample(range(n), r))
        return tuple(pool[i] for i in indices)

    @classmethod
    def random_combination_with_replacement(cls, iterable, r):
        "Random selection from itertools.combinations_with_replacement(iterable, r)"
        pool = tuple(iterable)
        n = len(pool)
        indices = sorted(random.randrange(n) for i in range(r))
        return tuple(pool[i] for i in indices)

    @classmethod
    def nth_combination(cls, iterable, r, index):
        'Equivalent to list(combinations(iterable, r))[index]'
        pool = tuple(iterable)
        n = len(pool)
        if r < 0 or r > n:
            raise ValueError
        c = 1
        k = min(r, n - r)
        for i in range(1, k + 1):
            c = c * (n - k + i) // i
        if index < 0:
            index += c
        if index < 0 or index >= c:
            raise IndexError
        result = []
        while r:
            c, n, r = c * r // n, n - 1, r - 1
            while index >= c:
                index -= c
                c, n = c * (n - r) // n, n - 1
            result.append(pool[-1 - n])
        return tuple(result)


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
    def list_pair2indexes_mother(cls, mother_list, child_list, ):
        n = len(mother_list)
        h = merge_dicts([{mother_list[i]: i} for i in range(n)],
                        vwrite=vwrite_no_duplicate_key)

        return [h[x] for x in child_list]



    @classmethod
    @LoggerToolkit.SEWrapper.info(func2logger=FoxylibLogger.func2logger)
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
        duplicate_list = IterToolkit.iter2duplicate_list(l, key=key)
        if not duplicate_list: return

        raise cls(duplicate_list)

class ListToolkit:
    @classmethod
    @IterToolkit.f_iter2f_list
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
        ix_list = list(ix_iter)

        assert_false(iter2duplicate_list(map(ig(0), ix_list)))

        n = len(ix_list)

        l = [None]*n
        for i,x in ix_list:
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
    def l_singleton2obj(cls, l, allow_empty_list=False):
        if len(l) == 1: return l[0]
        if not l and allow_empty_list: return None
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
        for xs_list in IterToolkit.zip_strict(*xs_ll):
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
    def kv2is_v_null(cls, kv):
        k, v = kv
        return v is None

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
            h_list_valid = lfilter(bool,h_iter)
            if not h_list_valid: return default

            h_final = reduce(lambda h1,h2: f_binary(h1,h2,*args,**kwargs), h_list_valid, {})
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
        def f_vresolve2f_vwrite(cls, f_vresolve):
            # this cannot not update dictionary
            def f_vwrite(h, k, v_in):
                v = f_vresolve(h, k, v_in)
                return DictToolkit.update_n_return(h, k, v)

            return f_vwrite

        @classmethod
        def f_vwrite2f_hvwrite(cls, f_vwrite):
            def f_hvwrite(h, k, v_in):
                v_h = h.get(k)

                are_all_dicts = all([isinstance(v_h, dict), isinstance(v_in, dict), ])
                if are_all_dicts:
                    v_out = merge_dicts([v_h, v_in], vwrite=f_hvwrite)
                    h_out = merge_dicts([h, {k: v_out}], vwrite=DictToolkit.VWrite.overwrite)
                else:
                    h_out = f_vwrite(h, k, v_in)

                return h_out

            return f_hvwrite

        @classmethod
        def no_duplicate_key(cls, h, k, v_in):
            if k not in h:
                return DictToolkit.update_n_return(h, k, v_in)

            raise DictToolkit.DuplicateKeyException({"key":k})

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
                    l = ListToolkit.lappend(h.get(k, []), v_in)
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
        def overwrite(cls, h_iter,):
            return cls.merge_dicts(list(h_iter), vwrite=DictToolkit.VWrite.overwrite)




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


class SingletonToolkit:
    class NotSingletonError(Exception):
        @classmethod
        def chk_n_raise(cls, obj_list,): # f_obj_list2errorstr=None, ):
            if obj_list and len(obj_list) == 1:
                return l_singleton2obj(obj_list)

            raise cls()

    class NoObjectError(Exception):
        @classmethod
        def chk_n_raise(cls, obj_list,): #f_obj_list2errorstr=None, ):
            if obj_list: return obj_list

            raise cls()

    class TooManyObjectsError(Exception):
        @classmethod
        def chk_n_raise(cls, obj_list, count): #, f_obj_list2errorstr=None, ):
            if (not obj_list) or len(obj_list) <= count: return obj_list

            raise cls()

class LLToolkit:
    @classmethod
    def _ll2flat_dim(cls, ll, count_unwrap):
        if count_unwrap < 0: raise Exception()
        if count_unwrap == 0: return (ll, len(ll))

        flat_dim_list = [cls._ll2flat_dim(l, count_unwrap - 1) for l in ll]
        (flat_ll, dim) = lmap(list, IterToolkit.zip_strict(*flat_dim_list))

        flat_list = lchain(*flat_ll)

        return (flat_list, dim)

    @classmethod
    def ll2flat(cls, ll, count_unwrap):
        flat_list, dim = cls._ll2flat_dim(ll, count_unwrap)
        return flat_list

    @classmethod
    def _flat_dim2ll_count(cls, flat_list, dim):
        if not isinstance(dim, list):
            return (flat_list[:dim], dim)

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

        l = filter2first(is_not_none, ll)
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

NotSingletonError = SingletonToolkit.NotSingletonError
NoObjectError = SingletonToolkit.NoObjectError
TooManyObjectsError = SingletonToolkit.TooManyObjectsError

iter2singleton = IterToolkit.iter2singleton
list2singleton = IterToolkit.iter2singleton

iter2singleton_or_none = IterToolkit.iter2singleton_or_none

uniq = IterToolkit.uniq
iuniq = IterToolkit.uniq
luniq = funcs2piped([IterToolkit.uniq, list])

iter2duplicate_list = IterToolkit.iter2duplicate_list
lfilter_duplicate = IterToolkit.iter2duplicate_list

sfilter = funcs2piped([filter, set])

l_singleton2obj = ListToolkit.l_singleton2obj
iter_singleton2obj = funcs2piped([list, ListToolkit.l_singleton2obj])

filter2singleton = IterToolkit.filter2singleton
filter2single_or_none = IterToolkit.filter2single_or_none

f_iter2f_list = IterToolkit.f_iter2f_list

map2singleton = IterToolkit.map2singleton

filter2first = IterToolkit.filter2first
lslice = IterToolkit.lslice

li2v = ListToolkit.li2v

hfilter = DictToolkit.filter

merge_dicts = DictToolkit.Merge.merge_dicts
dicts_overwrite = DictToolkit.Merge.overwrite

vwrite_no_duplicate_key = DictToolkit.VWrite.no_duplicate_key
vwrite_update_if_identical = DictToolkit.VWrite.update_if_identical
vwrite_overwrite = DictToolkit.VWrite.overwrite

f_vwrite2f_hvwrite = DictToolkit.VWrite.f_vwrite2f_hvwrite

lappend = ListToolkit.lappend
list2tuple = ListToolkit.list2tuple

chain_each = ListToolkit.chain_each
intersperse = ListToolkit.intersperse


ichain = chain
lchain = funcs2piped([chain, list])
schain = funcs2piped([chain, set])

lreversed = funcs2piped([reversed, list])

luniqchain = funcs2piped([chain, iuniq, list])

lchain.from_iterable = funcs2piped([chain.from_iterable, list])

smap = funcs2piped([map, set])
lmap_singleton = funcs2piped([lmap, l_singleton2obj])

lproduct = funcs2piped([product,list])

zip_strict = IterToolkit.zip_strict
lzip_strict = funcs2piped([zip_strict, list])

map_strict = IterToolkit.map_strict
lmap_strict = funcs2piped([map_strict, list])


# LLToolkit
f_batch_n2f_ll = LLToolkit.f_batch_n2f_ll
llmap_batch = LLToolkit.llmap_batch

llmap = LLToolkit.llmap
llfilter = LLToolkit.llfilter
llchain = LLToolkit.llchain
ll_depths2lchained = LLToolkit.ll_depths2lchained
transpose = LLToolkit.transpose

iter_func2suffixed = IterToolkit.iter_func2suffixed

bisect_by = IterToolkit.bisect_by
nsect_by = IterToolkit.nsect_by
