from foxylib.tools.function.function_tool import funcs2piped


class IndexToolkit:
    @classmethod
    def filter_by_indexes(cls, l, i_iter):
        for i in i_iter:
            yield l[i]

filter_by_indexes = IndexToolkit.filter_by_indexes
lfilter_by_indexes = funcs2piped([filter_by_indexes, list])