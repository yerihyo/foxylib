from functools import reduce
from math import floor

from foxylib.tools.collections.collections_tool import merge_dicts, DictTool


class CryptoTool:
    @classmethod
    def ciphertext2rehashed(cls, code_from: dict, hashspace_to: dict):
        q = len(hashspace_to['alphabet'])
        spacesize_to = pow(q, hashspace_to['digit'])

        dict_char2index = merge_dicts(
            [{c: i} for i, c in enumerate(code_from['alphabet'])],
            DictTool.VWrite.no_duplicate_key,
        )

        value = reduce(
            lambda v, c: (dict_char2index[c] + len(code_from['alphabet']) * v) % spacesize_to,
            code_from['key'],
            0,
        )

        [r,chars] = reduce(
            lambda vl, i: [floor(vl[0]/q), [hashspace_to['alphabet'][vl[0]%q], *vl[1]]],
            range(hashspace_to['digit']),
            [value, []],
        )
        return ''.join(chars)