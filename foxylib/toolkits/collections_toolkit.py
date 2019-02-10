from foxylib.toolkits.builtin_toolkit import pipe_funcs


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