import copy


class CoroTool:
    @classmethod
    def coro2ready(cls, coro):
        coro.send(None)
        return coro

    @classmethod
    def send2max(cls):
        from foxylib.tools.collections.collections_tool import AbsoluteOrder

        m = None
        while True:
            v = yield m
            m = max([m, v], key=AbsoluteOrder.null2min)

    @classmethod
    def send2dict_value2latest_occur_index(cls):
        from foxylib.tools.collections.iter_tool import IterTool

        h_value2latest_index = {}
        for i in IterTool.range_inf():
            v = yield copy.copy(h_value2latest_index)
            h_value2latest_index[v] = i
