from unittest import TestCase

from foxylib.tools.lexer.args_kwargs_lexer import ArgsKwargsLexer


class ArgsKwargsLexerTest(TestCase):
    def test_success_01(self):
        s = '"los angeles" nickname="L. A."'
        hyp = ArgsKwargsLexer.str2args_kwargs_pair(s)
        ref = (['los angeles'], {'nickname': 'L. A.'})
        self.assertEqual(hyp, ref)

    def test_success_02(self):
        s = '"los angeles" "santa barbara" tags="L. A.","San Francisco", "S.F."'
        hyp = ArgsKwargsLexer.str2args_kwargs_pair(s)
        ref = (['los angeles', 'santa barbara'], {'tags': '"L. A.","San Francisco", "S.F."'})
        self.assertEqual(hyp, ref)