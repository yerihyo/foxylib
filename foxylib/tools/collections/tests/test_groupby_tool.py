import json
import logging
from operator import itemgetter as ig
from pprint import pprint
from unittest import TestCase

from future.utils import lmap

from foxylib.tools.collections.groupby_tool import gb_tree_global, dict_groupby_tree, GroupbyTool
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
               ('b',
                [('d',
                  [('e', ['bde']),
                   ('g', ['bdgef']),
                   ('w', ['bdwege']),
                   ('a', ['bdasdf']),
                   ]
                  ),
                 ('e',
                  [('d', ['bed', 'bedfwef'])]
                  )
                 ]
                ),
               ('c',
                [('s', [('d', ['csdfe'])]),
                 ('d', [('s', ['cdsfe'])])
                 ]
                ),
               ('d',
                [('e', [('f', ['defdad'])])]
                )
               ]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_02(self):
        l = ["asdf","ade","abe","bde","bed","bdgef","bdwege","bedfwef","bdasdf","csdfe","defdad","cdsfe"]

        hyp = gb_tree_global(l, [ig(0), ig(1), ig(2)], leaf_func=lambda _l: lmap(lambda s: s[3:], _l))
        ref = [('a',
                [('s', [('d', ['f'])]),
                 ('d', [('e', [''])]),
                 ('b', [('e', [''])])
                 ]),
               ('b',
                [('d',
                  [('e', ['']),
                   ('g', ['ef']),
                   ('w', ['ege']),
                   ('a', ['sdf'])
                   ]),
                 ('e',
                  [('d', ['', 'fwef'])]
                  )]
                ),
               ('c',
                [('s', [('d', ['fe'])]),
                 ('d', [('s', ['fe'])])
                 ]),
               ('d', [('e', [('f', ['dad'])])])
               ]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_03(self):
        l = ["asdf","ade", "abe", "bde", "bed", "bdgef", "bdwege", "bedfwef", "bdasdf", "csdfe", "defdad", "cdsfe"]

        hyp = dict_groupby_tree(l, [ig(0), ig(1), ig(2)], )
        ref = {'a': {'b': {'e': ['abe']}, 'd': {'e': ['ade']}, 's': {'d': ['asdf']}},
               'b': {'d': {'a': ['bdasdf'], 'e': ['bde'], 'g': ['bdgef'], 'w': ['bdwege']},
                     'e': {'d': ['bed', 'bedfwef']}},
               'c': {'d': {'s': ['cdsfe']}, 's': {'d': ['csdfe']}},
               'd': {'e': {'f': ['defdad']}}}

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_04(self):
        hyp1 = GroupbyTool.objects2ordered_groups(range(10), lambda x:x%4, [0,1,2,3], )
        ref1 = [[0, 4, 8], [1, 5, 9], [2, 6], [3, 7]]
        self.assertEqual(hyp1, ref1)

    def test_05(self):
        h1 = GroupbyTool.iter2dicttree(range(10), [lambda x: x % 4])

        hyp1 = GroupbyTool.tree2aligned_list(h1, [[0, 1, 2, 3]])
        ref1 = [[0, 4, 8], [1, 5, 9], [2, 6], [3, 7]]
        self.assertEqual(hyp1, ref1)

        hyp2 = GroupbyTool.tree2aligned_list(h1, [[3, 2, 1, 0]])
        ref2 = [[3, 7], [2, 6], [1, 5, 9], [0, 4, 8]]
        self.assertEqual(hyp2, ref2)

        h3 = GroupbyTool.iter2dicttree(range(20), [lambda x: x % 3, lambda x: x % 4])
        hyp3 = GroupbyTool.tree2aligned_list(h3, [[2, 1, 0], [0, 1, 2, 3]])
        ref3 = [[[8], [5, 17], [2, 14], [11]],
                [[4, 16], [1, 13], [10], [7, 19]],
                [[0, 12], [9], [6, 18], [3, 15]]]
        self.assertEqual(hyp3, ref3)

        h4 = GroupbyTool.iter2dicttree([0, 1], [lambda x: x % 3])
        hyp4 = GroupbyTool.tree2aligned_list(h4, [[0, 1, 2]])
        ref4 = [[0], [1], []]
        self.assertEqual(hyp4, ref4)

        h5 = GroupbyTool.iter2dicttree([], [lambda x: x % 3])
        hyp5 = GroupbyTool.tree2aligned_list(h5, [[0, 1, 2]])
        ref5 = [[], [], []]
        self.assertEqual(hyp5, ref5)

    def test_06(self):
        hyp1 = GroupbyTool.groupby_tree_global_ordered(
            range(20),
            [lambda x: x % 3, lambda x: x % 4],
            [[0,1,2,],[3,2,1,0]],
        )
        ref1 = [[[3, 15], [6, 18], [9], [0, 12]],
                [[7, 19], [10], [1, 13], [4, 16]],
                [[11], [2, 14], [5, 17], [8]]]
        self.assertEqual(hyp1, ref1)
