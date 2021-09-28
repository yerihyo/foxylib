import copy
import logging
import random
from collections import deque
from itertools import chain, islice, count, groupby, repeat, starmap, tee, \
    zip_longest, cycle, filterfalse, combinations, takewhile, dropwhile
from operator import itemgetter as ig, mul
from pprint import pformat
from typing import TypeVar, Iterable, Callable, Any, List

from future.utils import lfilter, lmap
from nose.tools import assert_is_not_none, assert_equal, assert_less_equal

from foxylib.tools.coroutine.coro_tool import CoroTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import is_not_none
from foxylib.tools.nose.nose_tool import assert_all_same_length

T = TypeVar("T")

class IterTool:
    @classmethod
    def is_iterable(cls, x):
        try:
            iter(x)
            return True
        except TypeError:
            return False

    # iterable

    @classmethod
    def iter2dict(cls, iterable, key):
        from foxylib.tools.collections.collections_tool import merge_dicts, \
            vwrite_no_duplicate_key

        h_out = merge_dicts([{key(x): x} for x in iterable],
                            vwrite=vwrite_no_duplicate_key)
        return h_out

    @classmethod
    def iter2dict_value2index(cls, iterable):
        from foxylib.tools.collections.collections_tool import merge_dicts, \
            vwrite_no_duplicate_key

        h_out = merge_dicts([{x: i} for i, x in enumerate(iterable)],
                            vwrite=vwrite_no_duplicate_key)
        return h_out

    @classmethod
    def is_sorted(cls, keys):
        k0 = None

        is_first = True
        for k1 in keys:
            if is_first:
                is_first = False
            else:
                if k0 > k1:
                    return False

            k0 = k1

        return True

    @classmethod
    def values2bucketindexes(
            cls,
            values_sorted: Iterable[T],
            f_verifiers: List[Callable[[T], bool]],
    ):
        p = len(f_verifiers)
        j = 0
        v_prev = None

        for i, v in enumerate(values_sorted):
            if i != 0:
                assert_less_equal(v_prev, v)
            v_prev = v

            j = cls.first_true(range(j, p), default=p, pred=lambda jj:  f_verifiers[jj](v),)
            yield j





    @classmethod
    def exclude_none(cls, iter):
        yield from filter(is_not_none, iter)

    @classmethod
    def duplicates(cls, iterable):
        h = {}
        for i, x in enumerate(iterable):
            indexes_prev = h.get(x) or []
            indexes_cur = list(chain(indexes_prev, [i]))
            if indexes_prev:
                yield {"indexes":indexes_cur, 'value':x}

            h[x] = indexes_cur



    @classmethod
    def iter_uniq2set(cls, iter):
        l = list(iter)
        s = set(l)

        assert_equal(len(l), len(s))
        return s

    @classmethod
    def iter2list(cls, iterable):
        if not iterable:
            return []

        return list(iterable)

    @classmethod
    def value_units2index_largest_fit(cls, v, units):
        for i, unit in enumerate(units):
            if v >= unit:
                return i
        return None

    @classmethod
    def is_empty(cls, iterable):
        for _ in iterable:
            return False
        return True

    # doesn't work
    # @classmethod
    # def is_empty_yoo(iterable_in):
    #     for x in iterable_in:
    #         # iterable_out = chain([x], iterable_in)
    #         return False, iterable_in
    #     return True, []

    @classmethod
    def iter2is_empty(cls, iterable):
        return cls.is_empty(iterable)

    @classmethod
    def iter2has_item(cls, iterable):
        return not cls.is_empty(iterable)

    @classmethod
    def iter2chunks(cls, *_, **__):
        from foxylib.tools.collections.chunk_tool import ChunkTool
        yield from ChunkTool.iter2chunks(*_, **__)

    @classmethod
    def range_inf(cls):
        i = 0
        while True:
            yield i
            i += 1

    @classmethod
    def iter2dict_value2first_index_series(cls, iterable):
        coro = CoroTool.coro2ready(CoroTool.send2dict_value2first_occur_index())

        for v in iterable:
            yield coro.send(v)

    @classmethod
    def iter2dict_value2first_index(cls, iterable):
        return cls.iter2last(cls.iter2dict_value2first_index_series(iterable))

    @classmethod
    def iter2dict_value2latest_index_series(cls, iterable):
        coro = CoroTool.coro2ready(CoroTool.send2dict_value2latest_occur_index())

        for v in iterable:
            yield coro.send(v)

    @classmethod
    def iter2dict_value2latest_index_series_OLD(cls, iterable):
        h_value2latest_index = {}
        for i, v in enumerate(iterable):
            h_value2latest_index[v] = i
            yield copy.copy(h_value2latest_index)

    @classmethod
    def list_func_count2index_list_continuous_valid(cls, l, f_valid, count_match):
        n = len(l)

        i_list_valid = lfilter(lambda i: all(f_valid(l[i + j]) for j in range(count_match)),
                               range(n - (count_match - 1)))
        return i_list_valid

    @classmethod
    def iter2sliding_window(cls, iterable, window_size):
        q = deque()
        for x in iterable:
            q.append(x)

            while len(q) >= window_size:
                yield tuple(islice(q, window_size))
                q.popleft()

    @classmethod
    def iter2buffered(cls, iterable, buffer_size):
        if not buffer_size:
            yield from iterable

        else:
            q = deque()
            for x in iterable:
                q.append(x)

                while len(q) > buffer_size:
                    yield q.popleft()

            while q:
                yield q.popleft()

    @classmethod
    def f_batch2f_iter(cls, f_batch, chunk_size):
        from foxylib.tools.collections.chunk_tool import ChunkTool

        def f_iter(iterable, *_, **__):
            for x_list in ChunkTool.grouper(chunk_size, iterable):
                y_list = f_batch(x_list, *_, **__)
                if y_list is not None:
                    yield from y_list

        return f_iter

    @classmethod
    def iter_func2suffixed(cls, iter, f):
        for x in iter:
            yield (x, f(x))

    @classmethod
    def iter_func2prefixed(cls, iter, f):
        for x in iter:
            yield (f(x), x)

    @classmethod
    def iter2last(cls, iterable):
        i_cur, v = None, None
        for i, x in enumerate(iterable):
            i_cur = i
            v = x

        assert_is_not_none(i_cur)  # if iterable is empty, i_cur is None. assert may not be necessary
        return v

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
        # logger = FoxylibLogger.func_level2logger(cls._iter2singleton, logging.DEBUG)

        if idfun is None:
            idfun = lambda x: x

        it = iter(iterable)
        try:
            v = next(it)
        except StopIteration:
            if empty2null:
                return None
            raise

        k_v = idfun(v)

        for x in it:
            k_x = idfun(x)
            if k_x != k_v:
                # logger.exception(pformat({'v': v, 'x': x, 'k_v': k_v, 'k_x': k_x, }))
                raise Exception({'v': v, 'x': x, 'k_v': k_v, 'k_x': k_x, })

        return v

    @classmethod
    def iter2singleton(cls, iterable, idfun=None, ):
        return cls._iter2singleton(iterable, idfun=idfun, empty2null=False)

    @classmethod
    def iter2singleton_or_none(cls, iterable, idfun=None, ):
        return cls._iter2singleton(iterable, idfun=idfun, empty2null=True)

    @classmethod
    def are_all_equal(cls, iterable):
        for i, x in enumerate(cls.unique_justseen(iterable)):
            if i>0:
                return False
        return True

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
    def uniq(cls, seq: Iterable[T], idfun: Callable[[T], Any] = None) -> Iterable[T]:
        seen = set()
        if idfun is None:
            for x in seq:
                if x in seen:
                    continue
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
        return list(islice(iter, n))

    @classmethod
    def f_iter2f_list(cls, f_iter):
        def f_list(*_, **__):
            return list(f_iter(*_, **__))

        return f_list

    @classmethod
    def count(cls, iterable):
        return sum(1 for _ in iterable)

    @classmethod
    def has_more_than(cls, iterable, n):
        for i, _ in enumerate(iterable):
            if i >= n:
                return True
        return False

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
        if iterable is None:
            return None

        l = cls.head(1, iterable)
        if not l:
            return None
        return l[0]

    @classmethod
    def head_unless_null(cls, n, iterable):
        if n is None:
            return list(iterable)

        return cls.head(n, iterable)

    # from https://docs.python.org/3/library/itertools.html#itertools-recipes
    @classmethod
    def head(cls, n, iterable):
        return cls.take(n, iterable)

    @classmethod
    def take(cls, n, iterable):
        "Return first n items of the iterable as a list"
        if n is None:
            return list(iterable)

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
        return iter(deque(iterable, maxlen=n))

    @classmethod
    def consume(cls, iterator, n=None):
        if iterator is None:
            return

        "Advance the iterator n-steps ahead. If n is None, consume entirely."
        # Use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length deque
            deque(iterator, maxlen=0)
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
    def dotproduct(cls, vec1, vec2, sum=sum, map=map, mul=mul):
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
    def first_true(cls, iterable, default=None, pred=None):
        """Returns the first true value in the iterable.

        If no true value is found, returns *default*

        If *pred* is not None, returns the first item
        for which pred(item) is true.

        """
        # first_true([a,b,c], x) --> a or b or c or x
        # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
        return next(filter(pred, iterable), default)

    @classmethod
    def index_first_false(cls, iterable):
        return cls.count(takewhile(bool, iterable))
        # j = -1
        # for i, x in enumerate(iterable):
        #     if not x:
        #         return i
        #     j = i
        #
        # return j+1


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

    @classmethod
    def ordered2f_key(cls, ordered_iter):
        from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key

        h = merge_dicts([{v: i} for i, v in enumerate(ordered_iter)],
                        vwrite=vwrite_no_duplicate_key)
        return lambda x: h[x]


iter2singleton = IterTool.iter2singleton
exclude_none = IterTool.exclude_none
