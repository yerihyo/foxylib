from functools import reduce

from foxlib.toolkits.nose_toolkit import assert_all_same_length


def pipe_funcs(funcs):
    if not funcs: raise Exception()
    def f(*args, **kwargs):
        v_init = funcs[0](*args, **kwargs)
        v = reduce(lambda x, f:f(x), funcs[1:], v_init)
        return v
    return f

xrange = range
lrange = pipe_funcs([xrange, list])

imap = map
lmap = pipe_funcs([imap, list])
smap = pipe_funcs([imap, set])



ifilter = filter
lfilter = pipe_funcs([ifilter, list])
sfilter = pipe_funcs([ifilter, set])

iter2len = pipe_funcs([list, len])


izip = zip
lzip = pipe_funcs([izip, list])

def zip_strict(*list_of_list):
    assert_all_same_length(*list_of_list)
    return izip(*list_of_list)
izip_strict = zip_strict
lzip_strict = pipe_funcs([zip_strict, list])


def imap_strict(f, *list_of_iter):
    ll = lmap(list, list_of_iter)
    assert_all_same_length(ll)
    return imap(f, *ll)
lmap_strict = pipe_funcs([imap_strict, list])


def f_args2f_tuple(f_args):
    def f_tuple(args, **kwargs):
        return f_args(*args, **kwargs)
    return f_tuple
f_a2t = f_args2f_tuple

def check_length(*list_of_list):
    length_list = [len(l) for l in list_of_list]
    if len(set(length_list)) > 1: raise Exception(length_list)