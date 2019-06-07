from unittest import TestCase

from foxylib.tools.hangeul.hangeul_tools import HangeulToolkit


class HangeulToolkitTest(TestCase):
    def test_01(self):
        str_in = "나의 살던 고향은 꽃피는 산골~! >.<"
        hyp = HangeulToolkit.str2choseng(str_in)
        ref = "ㄴㅇ ㅅㄷ ㄱㅎㅇ ㄲㅍㄴ ㅅㄱ~! >.<"

        self.assertEqual(hyp, ref)
