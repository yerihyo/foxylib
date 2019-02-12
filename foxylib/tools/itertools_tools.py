from itertools import chain, product

from future.utils import lfilter, lmap

from foxylib.tools.builtin_tools import pipe_funcs
from foxylib.tools.collections_tools import iuniq, l_singleton2obj

ichain = chain
lchain = pipe_funcs([ichain, list])
schain = pipe_funcs([ichain, set])

luniqchain = pipe_funcs([ichain, iuniq, list])

lchain.from_iterable = pipe_funcs([ichain.from_iterable, list])

iter2len = pipe_funcs([list, len])
lfilter_singleton = pipe_funcs([lfilter, l_singleton2obj])
lmap_singleton = pipe_funcs([lmap, l_singleton2obj])

lproduct = pipe_funcs([product,list])


