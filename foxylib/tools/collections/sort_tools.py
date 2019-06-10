from operator import itemgetter as ig

from future.utils import lmap

from foxylib.tools.collections.collections_tools import lzip_strict
from foxylib.tools.function.function_tools import f_a2t


class SortToolkit:
    @classmethod
    def countingsorted(cls, iterable, f_key=None,
                       ):
        l = list(iterable)
        if not l: return l
        if f_key is None: f_key = lambda x: x

        n = len(l)
        key_obj_list = [(f_key(x), x)
                        for x in l]  # O(n)

        key_list = lmap(ig(0), key_obj_list)  # O(n)
        for k in key_list:  # O(n)
            if k < 0: raise Exception()

        m = max(key_list)  # O(n)
        counter = [0] * (m + 1)
        for key in key_list:  # O(n)
            counter[key] += 1

        index_list = [0] * (m + 1)
        total = 0
        for i, v in enumerate(counter):  # O(m)
            total += v
            index_list[i] = total

        l_result = [None] * n
        for key, obj in reversed(key_obj_list):  # O(n)
            i = index_list[key]
            l_result[i - 1] = obj
            index_list[key] -= 1

        #     for i,x in enumerate(l_result):
        #         if x is None: raise Exception(i)

        return l_result

    @classmethod
    def sorted_by_key_index(cls, l, f_key, ):
        key_list = lmap(f_key, l)
        h = dict(reversed([(key, i) for i, key in enumerate(key_list)]))

        key_obj_list = lzip_strict(key_list, l)

        f_key = f_a2t(lambda key, obj: h[key])
        # key_obj_list_sorted = SortToolkit.countingsorted(key_obj_list,f_key=f_key)
        key_obj_list_sorted = sorted(key_obj_list, key=f_key)

        l_sorted = lmap(ig(1), key_obj_list_sorted)
        return l_sorted
