from foxylib.tools.native.builtin_tools import pipe_funcs


class IndexToolkit:
    @classmethod
    def filter_by_indexes(cls, l, i_iter):
        for i in i_iter:
            yield l[i]

filter_by_indexes = IndexToolkit.filter_by_indexes
lfilter_by_indexes = pipe_funcs([filter_by_indexes, list])