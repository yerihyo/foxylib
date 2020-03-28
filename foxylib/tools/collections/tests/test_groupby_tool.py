import logging
from operator import itemgetter as ig
from pprint import pprint
from unittest import TestCase

from future.utils import lmap

from foxylib.tools.collections.groupby_tool import gb_tree_global
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestGroupbyTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        l = ["asdf","ade","abe","bde","bed","bdgef","bdwege","bedfwef","bdasdf","csdfe","defdad","cdsfe"]

        hyp = gb_tree_global(l, [ig(0), ig(1), ig(2)])
        ref = [('a',
                [('s', [('d', ['asdf'])]),
                 ('d', [('e', ['ade'])]),
                 ('b', [('e', ['abe'])]),
                 ]
                ),
               ('c',
                [('s', [('d', ['csdfe'])]),
                 ('d', [('s', ['cdsfe'])]),
                 ]
                ),
               ('b',
                [('e', [('d', ['bed', 'bedfwef'])]),
                 ('d',
                  [('e', ['bde']),
                   ('g', ['bdgef']),
                   ('w', ['bdwege']),
                   ('a', ['bdasdf']),
                   ]
                  )
                 ]
                ),
               ('d', [('e', [('f', ['defdad'])])])]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_02(self):
        l = ["asdf","ade","abe","bde","bed","bdgef","bdwege","bedfwef","bdasdf","csdfe","defdad","cdsfe"]

        hyp = gb_tree_global(l, [ig(0), ig(1), ig(2)], leaf_func=lambda l:lmap(lambda s:s[3:],l))
        ref = [('a',
                [('s', [('d', ['f'])]),
                 ('d', [('e', [''])]),
                 ('b', [('e', [''])]),
                 ]
                ),
               ('c',
                [('s', [('d', ['fe'])]),
                 ('d', [('s', ['fe'])]),
                 ]
                ),
               ('b',
                [('e', [('d', ['', 'fwef'])]),
                 ('d',
                  [('e', ['']),
                   ('g', ['ef']),
                   ('w', ['ege']),
                   ('a', ['sdf']),
                   ]
                  )
                 ]
                ),
               ('d', [('e', [('f', ['dad'])])])]

        # pprint(hyp)
        self.assertEqual(hyp, ref)