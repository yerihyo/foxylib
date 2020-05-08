from unittest import TestCase

from foxylib.tools.coroutine.coro_tool import CoroTool


class TestCoroTool(TestCase):
    def test_01(self):
        l = [1, 2, 7, 3, 4, 8, 6, 9]
        coro = CoroTool.coro2ready(CoroTool.send2max())

        hyp = [coro.send(x) for x in l]
        ref = [1, 2, 7, 7, 7, 8, 8, 9]

        # pprint({"hyp":hyp})
        self.assertEqual(hyp, ref)

    def test_02(self):
        l = [1, 2, 1, 2, 3, 2, 3, 2]
        coro = CoroTool.coro2ready(CoroTool.send2dict_value2latest_occur_index())

        hyp = [coro.send(x) for x in l]
        ref = [{1: 0},
               {1: 0, 2: 1},
               {1: 2, 2: 1},
               {1: 2, 2: 3},
               {1: 2, 2: 3, 3: 4},
               {1: 2, 2: 5, 3: 4},
               {1: 2, 2: 5, 3: 6},
               {1: 2, 2: 7, 3: 6}]

        # pprint({"hyp":hyp})
        self.assertEqual(hyp, ref)
