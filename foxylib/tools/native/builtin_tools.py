from functools import reduce

from future.utils import lmap

from foxylib.tools.nose.nose_tools import assert_all_same_length


def pipe_funcs(funcs):
    if not funcs: raise Exception()

    def f(*args, **kwargs):
        v_init = funcs[0](*args, **kwargs)
        v = reduce(lambda x, f: f(x), funcs[1:], v_init)
        return v

    return f


imap = map
smap = pipe_funcs([map, set])

ifilter = filter
sfilter = pipe_funcs([filter, set])

izip = zip
xrange = range

iter2len = pipe_funcs([list, len])
idfun = lambda x:x

def zip_strict(*list_of_list):
    assert_all_same_length(*list_of_list)
    return zip(*list_of_list)


izip_strict = zip_strict
lzip_strict = pipe_funcs([zip_strict, list])


def imap_strict(f, *list_of_iter):
    ll = lmap(list, list_of_iter)
    assert_all_same_length(ll)
    return map(f, *ll)


lmap_strict = pipe_funcs([imap_strict, list])


def f_args2f_tuple(f_args):
    def f_tuple(args, **kwargs):
        return f_args(*args, **kwargs)

    return f_tuple


f_a2t = f_args2f_tuple


def check_length(*list_of_list):
    length_list = [len(l) for l in list_of_list]
    if len(set(length_list)) > 1: raise Exception(length_list)


class BoolToolkit:
    @classmethod
    def parse_sign2bool(cls, s):
        if s == "+": return True
        if s == "-": return False
        raise Exception("Invalid sign: {0}".format(s))

class IntToolkit:
    @classmethod
    def parse_sign2int(cls, s):
        if not s: return 1
        if s == "+": return 1
        if s == "-": return -1
        raise Exception("Invalid sign: {0}".format(s))