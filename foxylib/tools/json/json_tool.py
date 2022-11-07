import copy
import json
import logging
from datetime import datetime
from decimal import Decimal
from functools import reduce
from pprint import pprint, pformat
from typing import List, Union, Any

import dateutil.parser
import yaml
from future.utils import lmap
from nose.tools import assert_true, assert_less_equal, assert_false

from foxylib.tools.collections.collections_tool import merge_dicts, DictTool, \
    vwrite_no_duplicate_key, lchain, smap, ListTool
from foxylib.tools.collections.traversile.traversile_tool import TraversileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import is_string


class Jstep:
    class Type:
        STRING = "string"
        INTEGER = "integer"

    @classmethod
    def jstep2type(cls, jstep):
        if is_string(jstep): return cls.Type.STRING
        if isinstance(jstep,int): return cls.Type.INTEGER
        assert "jnode with invalid type: {}".format(jstep)

    @classmethod
    def down(cls, j_in, k):
        if not j_in:
            return j_in

        if isinstance(j_in, dict):
            return j_in.get(k)

        if isinstance(j_in, list):
            assert(isinstance(k, int))
            return j_in[k]

        assert "Should not reach here!"

    class KV2J:
        @classmethod
        def default(cls, k, v):
            if isinstance(k, str):
                return {k: v}

            if isinstance(k, int):
                return lchain([None]*k, [v])

            assert "Should not reach here!"

        @classmethod
        def dict(cls, k, v):
            return {k: v}


# class Json2Native:
#     class Type:
#         DECIMAL = "decimal"
#         DATETIME = "datetime"
#         MONGO_OBJECTID = "mongo_objectid"
#
#     @classmethod
#     def value2native(cls, v, type_):
#         if isinstance(v, (list, set, tuple), ):
#             return type(v)([cls.value2native(x, type_) for x in v])
#
#         if type_ in {Decimal, cls.Type.DECIMAL}:
#             return Decimal(v)
#
#         if type_ in {datetime, cls.Type.DATETIME}:
#             return dateutil.parser.parse(v)
#
#         from bson import ObjectId
#         if type_ in {ObjectId, cls.Type.MONGO_OBJECTID}:
#             return dateutil.parser.parse(v)
#
#         raise NotImplementedError({'type_': type_})


class JsonTool:
    @classmethod
    def jpath2xpath(cls, jpath):
        return '.'.join(jpath)

    @classmethod
    def jpath_in(cls, jpath, jpaths):
        xpath = cls.jpath2xpath(jpath)
        xpaths = smap(cls.jpath2xpath, jpaths)
        return xpath in xpaths

    @classmethod
    def has_jpath(cls, j_in, jpath):
        try:
            JsonTool.down(j_in, jpath)
            return True
        except KeyError:
            return False

    @classmethod
    def keys2removed(cls, j_in, keys):
        from foxylib.tools.collections.dicttree.dicttree_tool import \
            DicttreeTool
        return DicttreeTool.keys2removed(j_in, keys)

    @classmethod
    def json2dictsorted(cls, jdoc_in):
        def dict2sorted(dict_in_):
            if not isinstance(dict_in_, dict):
                return dict_in_

            return DictTool.dict2sorted({k: cls.json2dictsorted(v)
                    for k, v in dict_in_.items()})

        dict_out = TraversileTool.tree2traversed(
            jdoc_in, dict2sorted, target_types={list, set, tuple})
        return dict_out


    # @classmethod
    # def func_types2f_traversile(cls, f, types=None):
    #     # traversile = while traversing  e.g. traversile conversion
    #     # mobile = while moving  e.g. mobile shooting
    #
    #     type_tuple = tuple(set(types)) if types is not None else None
    #
    #     def x2is_covered_type(x):
    #         if type_tuple is None:
    #             return True
    #
    #         return isinstance(x, type_tuple)
    #
    #     def f_traversing(x):
    #         if not x2is_covered_type(x):
    #             return f(x)
    #
    #         if isinstance(x, (dict,)):
    #             return {k: f_traversing(v) for k, v in x.items()}
    #
    #         if isinstance(x, (list, tuple, set)):
    #             return type(x)(map(f_traversing, x))
    #
    #         return f(x)
    #
    #     return f_traversing

    # @classmethod
    # def convert_traversile(cls, x_in, f_node, types=None):
    #     x_out = TraversileTool.tree2traversed(x_in, f_node, target_types=types)
    #     return x_out

    @classmethod
    def transduce_kv(cls, x_in, transducer_tree, ):
        logger = FoxylibLogger.func_level2logger(
            cls.transduce_kv, logging.DEBUG)

        if not transducer_tree:
            return x_in

        if isinstance(x_in, (tuple, list, set, frozenset)):
            l_out = [cls.transduce_kv(x, transducer_tree) for x in x_in]
            x_out = type(x_in)(l_out)
            return x_out

        def kv2converted(k_in, v_in):
            if k_in not in transducer_tree:
                return {k_in: v_in}

            transducer_node = transducer_tree[k_in]

            if callable(transducer_node):
                return transducer_node(v_in)

            v_out = cls.transduce_kv(v_in, transducer_node)
            return {k_in: v_out}


        if isinstance(x_in, (dict,)):
            h_out = merge_dicts([
                kv2converted(k, v) for k, v in x_in.items()],
                vwrite=vwrite_no_duplicate_key)


            # h_out = merge_dicts([
            #     {k: cls.transduce_value(v, transducer_tree.get(k, {}))}
            #     for k, v in x_in.items()
            # ], vwrite=vwrite_no_duplicate_key)
            x_out = type(x_in)(h_out)
            return x_out

        return x_in

    @classmethod
    def transduce_value(cls, x_in, pinpoint_tree, ):
        # logger = FoxylibLogger.func_level2logger(
        #     cls.transduce_value, logging.DEBUG)

        # if not pinpoint_tree:
        #     return x_in
        # logger.debug({
        #     'x_in':x_in,
        #     'pinpoint_tree':pinpoint_tree,
        # })

        if not isinstance(pinpoint_tree, dict):
            assert_true(callable(pinpoint_tree))
            # logger.debug({'pinpoint_tree':pinpoint_tree, 'j_in':j_in})
            return pinpoint_tree(x_in)

        if isinstance(x_in, (tuple, list, set, frozenset)):
            l_out = [cls.transduce_value(x, pinpoint_tree) for x in x_in]
            x_out = type(x_in)(l_out)
            return x_out

        if isinstance(x_in, (dict,)):
            h_out = merge_dicts([
                {k: cls.transduce_value(v, pinpoint_tree.get(k, {}))}
                for k, v in x_in.items()
                if k in x_in
            ], vwrite=vwrite_no_duplicate_key)

            x_out = type(x_in)(h_out)
            return x_out

        return x_in

    # @classmethod
    # def dataobj2json(cls, *_, **__):
    #     return Json2Native.dataobj2json(*_, **__)

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
    def j2filepath(cls, j_in, filepath):
        from foxylib.tools.file.file_tool import FileTool
        FileTool.utf82file(json.dumps(j_in), filepath)

    @classmethod
    def down_or_error(cls, j, l, ):
        if not isinstance(l, list):
            raise ValueError({
                'message': 'input is not of list type.',
                'l': l,
            })

        for x in l:
            j = j[x]
        return j

    @classmethod
    def down(cls, j, l, default=None, strict=False):
        if not l:
            return j

        if (not strict) and (not j):
            return default

        for x in l:
            if isinstance(j, dict):
                if x not in j:
                    if not strict:
                        return default
            j = j[x]

        return j

    @classmethod
    def j_jpath2replaced(cls, jdoc_in: dict, jpath: List[Union[str, int]], value: Any) -> dict:
        if not jpath:
            return value

        jstep = jpath[0]
        if isinstance(jstep, int):
            assert_true(isinstance(jstep, int))
            assert_true(isinstance(jdoc_in, list))

            jchild_in = jdoc_in[jstep]
            jchild_out = cls.j_jpath2replaced(jchild_in, jpath[1:], value)
            jdoc_out = ListTool.splice(jdoc_in, (jstep, jstep + 1), [jchild_out])
            return jdoc_out

        if isinstance(jstep, str):
            assert_true(isinstance(jstep, str))
            assert_false(isinstance(jdoc_in, list))

            jchild_in = jdoc_in[jstep]
            jchild_out = cls.j_jpath2replaced(jchild_in, jpath[1:], value)
            jdoc_out = merge_dicts(
                [jdoc_in, {jstep: jchild_out}, ],
                vwrite=DictTool.VWrite.overwrite,
            )

            # if jpath == ['choices']:
            #     pprint({
            #         'value':value,
            #         'jpath':jpath,
            #         'jdoc_in': jdoc_in,
            #         'jchild_in': jchild_in,
            #         'jchild_out': jchild_out,
            #         'jdoc_out': jdoc_out,
            #     })
            #
            #     raise Exception()
            return jdoc_out

        raise ValueError({'jstep': jstep})

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
    def jpath_value2json(cls, jpath, v, kv2j=None):
        logger = FoxylibLogger.func_level2logger(cls.jpath_value2json, logging.DEBUG)

        if kv2j is None:
            kv2j = Jstep.KV2J.default

        # logger.debug({'jpath':jpath})
        assert_true(isinstance(jpath, (list, tuple)), )
        return reduce(lambda x, k: kv2j(k, x), reversed(jpath), v)

    @classmethod
    def jpath2filtered(cls, j_in, jpath):
        v = cls.down(j_in, jpath)
        j_out = cls.jpath_value2json(jpath, v)
        return j_out

    @classmethod
    def jpaths2filtered(cls, j_in, jpaths):
        j_list = lmap(lambda jpath: cls.jpath2filtered(j_in, jpath), jpaths)
        j_out = merge_dicts(j_list, vwrite=DictTool.VWrite.f_vwrite2f_hvwrite(vwrite_no_duplicate_key))
        return j_out

    @classmethod
    def j2utf8(cls, j, **__):
        return json.dumps(j, ensure_ascii=False, **__)


# jdown = JsonTool.down
