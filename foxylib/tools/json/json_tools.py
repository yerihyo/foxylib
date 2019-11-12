import copy
import json
from functools import reduce

import yaml
from future.utils import lmap
from nose.tools import assert_true

from foxylib.tools.collections.collections_tools import merge_dicts, DictToolkit, vwrite_no_duplicate_key
from foxylib.tools.log.logger_tools import LoggerToolkit, FoxylibLogger
from foxylib.tools.string.string_tools import is_string


class JStep:
    class Type:
        STRING = "string"
        INTEGER = "integer"

    @classmethod
    def jstep2type(cls, jstep):
        if is_string(jstep): return cls.Type.STRING
        if isinstance(jstep,int): return cls.Type.INTEGER
        assert "jnode with invalid type: {}".format(jstep)

    @classmethod
    def down(cls, j_in, jstep):
        if not j_in:
            return j_in

        t = cls.jstep2type(jstep)

        if t == cls.Type.STRING:
            return j_in.get(jstep)

        if t == cls.Type.INTEGER:
            return j_in[jstep]

        assert "Should not reach here!"

    @classmethod
    def jstep_v2j(cls, jstep, v):
        t = cls.jstep2type(jstep)

        if t == cls.Type.STRING:
            return {jstep:v}

        if t == cls.Type.INTEGER:
            return [v]

        assert "Should not reach here!"

class JToolkit:
    @classmethod
    def filepath2j(cls, filepath):
        from foxylib.tools.file.file_tools import FileToolkit
        utf8 = FileToolkit.filepath2utf8(filepath)
        if not utf8: return None

        j = json.loads(utf8)
        return j

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
        logger = FoxylibLogger.func2logger(cls.merge_list)
        #logger.info("j_list({0})".format(json.dumps(j_list, ensure_ascii=False)))
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

    @classmethod
    def j_jpaths2first(cls, j_in, jpaths, ):
        default = None

        if not j_in:
            return default

        for jpath in jpaths:
            v = cls.down(j_in,jpath)
            if v:
                return v

        return default

    @classmethod
    def j_leafs2first(cls, j_in, leafs,):
        jpath_list = lmap(lambda x:[x], leafs)
        return cls.j_jpaths2first(j_in, jpath_list)

    @classmethod
    def jpath_v2j(cls, jpath, v):
        assert_true(isinstance(jpath, list))
        return reduce(lambda x, jstep: JStep.jstep_v2j(jstep, x), reversed(jpath), v)

    @classmethod
    def _j_jpath2filtered(cls, j_in, jpath):
        v = cls.down(j_in, jpath)
        j_out = cls.jpath_v2j(jpath, v)
        return j_out

    @classmethod
    def j_jpaths2filtered(cls, j_in, jpaths):
        j_list = lmap(lambda jpath: cls._j_jpath2filtered(j_in, jpath), jpaths)
        j_out = merge_dicts(j_list, vwrite=DictToolkit.VWrite.f_vwrite2f_hvwrite(vwrite_no_duplicate_key))
        return j_out

    @classmethod
    def j2utf8(cls, j, **__):
        return json.dumps(j, ensure_ascii=False, **__)


jdown = JToolkit.down
