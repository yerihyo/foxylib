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


sfilter = pipe_funcs([filter, set])

iter2len = pipe_funcs([list, len])
idfun = lambda x:x




def check_length(*list_of_list):
    length_list = [len(l) for l in list_of_list]
    if len(set(length_list)) > 1: raise Exception(length_list)




class NoneToolkit:
    @classmethod
    def is_none(cls, x): return x is None

    @classmethod
    def is_not_none(cls, x): return x is not None

    @classmethod
    def is_all_none(cls, l): return all(map(cls.is_none, l))

class BooleanToolkit:
    @classmethod
    def parse_sign2bool(cls, s):
        if s == "+": return True
        if s == "-": return False
        raise Exception("Invalid sign: {0}".format(s))

    @classmethod
    def parse2nullboolean(cls, s):
        if any(filter(lambda x:s is x,{None, True, False})):
            return s

        if not s: return None

        s_lower = s.lower()
        if s_lower.isdecimal():
            v = int(s_lower)
            return bool(v)

        if s_lower in {"true", "t", "yes", "y",}: return True
        if s_lower in {"false", "f", "no", "n",}: return False
        return None

class IntToolkit:
    @classmethod
    def parse_sign2int(cls, s):
        if not s: return 1
        if s == "+": return 1
        if s == "-": return -1
        raise Exception("Invalid sign: {0}".format(s))

is_none = NoneToolkit.is_none
is_not_none = NoneToolkit.is_not_none
is_all_none = NoneToolkit.is_all_none