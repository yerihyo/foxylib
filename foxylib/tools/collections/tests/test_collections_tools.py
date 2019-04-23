from pprint import pprint
from unittest import TestCase

import numpy

from foxylib.tools.collections.collections_tools import LLToolkit, transpose


class LLToolkitTest(TestCase):
    def test_01(self):
        ll = [[["{0}{1}{2}".format(i+1,j+1,k+1)
                for k in range(2)]
               for j in range(3)]
              for i in range(4)]


        hyp1 = LLToolkit.ll_depths2lchained(ll, [1])
        # pprint(hyp1)
        ref1 = [['111', '112', '121', '122', '131', '132'],
                ['211', '212', '221', '222', '231', '232'],
                ['311', '312', '321', '322', '331', '332'],
                ['411', '412', '421', '422', '431', '432']]

        self.assertEqual(hyp1, ref1)

        hyp2 = LLToolkit.ll_depths2lchained(ll, [0])
        # pprint(hyp2)
        ref2 = [['111', '112'],
                ['121', '122'],
                ['131', '132'],
                ['211', '212'],
                ['221', '222'],
                ['231', '232'],
                ['311', '312'],
                ['321', '322'],
                ['331', '332'],
                ['411', '412'],
                ['421', '422'],
                ['431', '432']]
        self.assertEqual(hyp2, ref2)

        hyp3 = LLToolkit.ll_depths2lchained(ll, [0,1])
        # pprint(hyp3)
        ref3 = ['111', '112',
                '121', '122',
                '131', '132',
                '211', '212',
                '221', '222',
                '231', '232',
                '311', '312',
                '321', '322',
                '331', '332',
                '411', '412',
                '421', '422',
                '431', '432']
        self.assertEqual(hyp3, ref3)

    def test_02(self):
        s_K_list_J_list_I_list = [[["{0}{1}{2}".format(i + 1, j + 1, k + 1)
                                    for k in range(2)]
                                   for j in range(3)]
                                  for i in range(4)]

        s_I_list_K_list_J_list = transpose(s_K_list_J_list_I_list, [1, 2, 0])
        hyp = s_I_list_K_list_J_list
        # pprint(hyp)
        ref = [[['111', '211', '311', '411'], # K
                ['112', '212', '312', '412']], # J
               [['121', '221', '321', '421'],
                ['122', '222', '322', '422']],
               [['131', '231', '331', '431'],
                ['132', '232', '332', '432']]]
        self.assertEqual(hyp, ref)