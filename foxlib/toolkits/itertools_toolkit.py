from itertools import chain, product

from future.utils import lfilter, lmap

from foxlib.toolkits.builtin_toolkit import pipe_funcs
from foxlib.toolkits.collections_toolkit import iuniq, l_singleton2obj

ichain = chain
lchain = pipe_funcs([ichain, list])
schain = pipe_funcs([ichain, set])

luniqchain = pipe_funcs([ichain, iuniq, list])

# ichain.from_iterable = chain.from_iterable # not necessary
lchain.from_iterable = pipe_funcs([ichain.from_iterable, list])

# iter2len = pipe_funcs([list, len])
lfilter_singleton = pipe_funcs([lfilter, l_singleton2obj])
lmap_singleton = pipe_funcs([lmap, l_singleton2obj])

lproduct = pipe_funcs([product,list])


