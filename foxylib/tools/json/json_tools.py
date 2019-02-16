import copy
import json
from functools import reduce

import yaml

from foxylib.tools.file_tools import FileToolkit
from foxylib.tools.logger_tools import LoggerToolkit


class JToolkit:
    @classmethod
    def jkey_v2json(cls, l, v_IN):
        j_OUT = reduce(lambda j, k: {k: j}, reversed(l), v_IN)
        return j_OUT

    @classmethod
    def down_or_error(cls, j, l, ):
        for x in l:
            j = j[x]
        return j

    @classmethod
    def down(cls, j, l, default=None, ):
        if not j: return default

        for x in l:
            if x not in j: return default
            j = j[x]

        return j

    @classmethod
    def update(cls, j, l, v, default=None, ):
        n = len(l)
        for i in range(n - 1):
            if not j: return default
            if l[i] not in j: return default
            j = j[l[i]]

        j[l[-1]] = v

        return j

    @classmethod
    def down_any(cls, j, ll, default=None, ):
        for l in ll:
            try:
                return cls.down_or_error(j, l)
            except KeyError:
                continue
        return default

    @classmethod
    def down_first(cls, j, key_ll, default=None, ):
        for key_list in key_ll:
            try:
                return cls.down_or_error(j, key_list)
            except KeyError:
                pass

        return default

    @classmethod
    def down_or_create(cls, j_IN, l, ):
        j = j_IN
        for x in l:
            if not j: raise Exception()
            if x not in j: j[x] = {}
            j = j[x]

        return j

    @classmethod
    def merge_list(cls, j_list):
        logger = LoggerToolkit.f_class2logger(cls.merge_list)
        logger.info("j_list({0})".format(json.dumps(j_list, ensure_ascii=False)))
        if not j_list: return None

        j1 = copy.deepcopy(j_list[0])
        j_MERGED = reduce(lambda j_BASE, j: cls.merge2(j_BASE, j), j_list[1:], j1)
        return j_MERGED

    @classmethod
    def merge2(cls, j_BASE, j_NEW, ):
        return cls._merge2_helper(j_BASE, j_NEW, [])

    class MergeConflictException(Exception): pass

    @classmethod
    def _merge2_helper(cls, j_BASE, j_NEW, key_history):
        if not isinstance(j_NEW, dict):
            raise cls.MergeConflictException(".".join(key_history))

        for k, v in j_NEW.items():
            if k not in j_BASE:
                j_BASE[k] = v
                continue

            cls._merge2_helper(j_BASE[k], j_NEW[k], key_history + [k])
        return j_BASE

jdown = JToolkit.down