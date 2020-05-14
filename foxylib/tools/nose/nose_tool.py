from pprint import pformat


class AssertTool:
    @classmethod
    def assert_all_same(cls, l):
        if not l: return

        n = len(l)
        for i in range(1,n):
            if l[i]!=l[0]:
                assert False, "Different object at index {0} in {1}".format(i, pformat(l))

    @classmethod
    def assert_all_same_length(cls, *list_of_list):
        length_list = [len(l) for l in list_of_list]
        if len(set(length_list)) > 1: raise Exception(length_list)


assert_all_same = AssertTool.assert_all_same
assert_all_same_length = AssertTool.assert_all_same_length