import copy
import json
import logging
from datetime import datetime
from decimal import Decimal
from functools import reduce
from pprint import pprint

import dateutil.parser
import yaml
from future.utils import lmap
from nose.tools import assert_true

from foxylib.tools.collections.collections_tool import merge_dicts, DictTool, vwrite_no_duplicate_key, lchain
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import is_string


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


class Json2Native:
    class Type:
        DECIMAL = "decimal"
        DATETIME = "datetime"
        MONGO_OBJECTID = "mongo_objectid"

    @classmethod
    def value2native(cls, v, type_):
        if isinstance(v, (list, set, tuple), ):
            return type(v)([cls.value2native(x, type_) for x in v])

        if type_ in {Decimal, cls.Type.DECIMAL}:
            return Decimal(v)

        if type_ in {datetime, cls.Type.DATETIME}:
            return dateutil.parser.parse(v)

        from bson import ObjectId
        if type_ in {ObjectId, cls.Type.MONGO_OBJECTID}:
            return dateutil.parser.parse(v)

        raise NotImplementedError({'type_': type_})

    @classmethod
    def json2native(cls, j_in, type_tree, value2native=None):
        logger = FoxylibLogger.func_level2logger(cls.json2native, logging.DEBUG)

        # logger.debug({'j_in': j_in, 'type_tree': type_tree,
        #               'value2native': value2native})

        if value2native is None:
            value2native = cls.value2native

        if not isinstance(type_tree, dict):
            return value2native(j_in, type_tree)

        if isinstance(j_in, list):
            h_out = [cls.json2native(x, type_tree)
                     for x in j_in]
            return h_out
        if isinstance(j_in, dict):
            h_out = merge_dicts([
                {k: cls.json2native(v, type_tree.get(k, {}))}
                for k, v in j_in.items()],
                vwrite=vwrite_no_duplicate_key)
            return h_out

        return j_in


class JsonTool:
    @classmethod
    def json2native(cls, *_, **__):
        return Json2Native.json2native(*_, **__)

    @classmethod
    def native2json(cls, *_, **__):
        return Json2Native.json2native(*_, **__)


    @classmethod
    def merge_list(cls, *_, **__):
        return DictTool.Merge.merge_dicts(*_, **__)

    @classmethod
    def filepath2j(cls, filepath):
        logger = FoxylibLogger.func_level2logger(cls.filepath2j, logging.DEBUG)
        logger.debug({"filepath":filepath})

        from foxylib.tools.file.file_tool import FileTool
        utf8 = FileTool.filepath2utf8(filepath)
        if not utf8: return None

        j = json.loads(utf8)
        return j

    @classmethod
    def down_or_error(cls, j, l, ):
        for x in l:
            j = j[x]
        return j

    @classmethod
    def down(cls, j, l, default=None, strict=False):
        if (not strict) and (not j):
            return default

        for x in l:
            if (not strict) and (x not in j):
                return default
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
    def down_or_lazycreate(cls, j_in, jpath, f_default=None):
        logger = FoxylibLogger.func_level2logger(cls.down_or_lazycreate,
                                                 logging.DEBUG)

        if f_default is None:
            f_default = lambda: None

        j = j_in
        n = len(jpath)

        for i in range(n):
            jstep = jpath[i]

            # logger.debug({"i":i, "j":j, "jstep":jstep})
            if j is None:
                raise Exception()

            if jstep not in j:
                v = {} if i+1 < n else f_default()
                j[jstep] = v

            j = j[jstep]

        return j

    @classmethod
    def down_or_create(cls, j_in, jpath, default=None):
        return cls.down_or_lazycreate(j_in, jpath, lambda: default)

    @classmethod
    def j_jpath2pop(cls, j, jpath, default=None):
        if not jpath:
            return j

        j_node = cls.down(j, jpath[:-1])
        # pprint(j_node)
        return j_node.pop(jpath[-1], default)

    @classmethod
    def j_jpath2popped(cls, j, jpath):
        cls.j_jpath2pop(j, jpath)
        return j

    @classmethod
    def j_jpaths2popped(cls, j, jpath_list):
        return reduce(lambda x, jpath: cls.j_jpath2popped(x, jpath),
                      jpath_list,
                      j)

    @classmethod
    def j_jpaths2excluded(cls, j, jpath_list):
        return cls.j_jpaths2popped(copy.deepcopy(j), jpath_list)

    @classmethod
    def j_jpath2excluded(cls, j, jpath):
        return cls.j_jpaths2excluded(j, [jpath])

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
        j_out = merge_dicts(j_list, vwrite=DictTool.VWrite.f_vwrite2f_hvwrite(vwrite_no_duplicate_key))
        return j_out

    @classmethod
    def j2utf8(cls, j, **__):
        return json.dumps(j, ensure_ascii=False, **__)


jdown = JsonTool.down
jpath_v2j = JsonTool.jpath_v2j
