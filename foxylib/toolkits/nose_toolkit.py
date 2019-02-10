from pprint import pformat


def assert_all_same(l):
    if not l: return

    n = len(l)
    for i in range(1,n):
        if l[i]!=l[0]:
            assert False, "Different object at index {0} in {1}".format(i, pformat(l))


def assert_all_same_length(*list_of_list):
    length_list = [len(l) for l in list_of_list]
    if len(set(length_list)) > 1: raise Exception(length_list)