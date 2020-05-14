from unittest import TestCase

from foxylib.tools.hangeul.hangeul_tool import HangeulTool


class HangeulToolTest(TestCase):
    def test_01(self):
        str_in = "나의 살던 고향은 꽃피는 산골~! >.<"
        hyp = HangeulTool.str2compatibility_choseung(str_in)
        ref = "ㄴㅇ ㅅㄷ ㄱㅎㅇ ㄲㅍㄴ ㅅㄱ~! >.<"

        self.assertEqual(hyp, ref)


    def test_02(self):
        str_in = "판"
        hyp = HangeulTool.str2compatibility_choseung(str_in)
        ref = "ㅍ"

        self.assertEqual(hyp, ref)
