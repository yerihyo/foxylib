import logging

from nose.tools import assert_is

from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.collections.dicttree.dicttree_tool import DicttreeTool
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.collections.traversile.traversile_tool import TraversileTool, \
    TraverseFailError
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.typing.typing_tool import TypingTool


# class SchemaKey:
#     class Oneof:
#         pass

# class SchemaOperator:
#     @classmethod
#     def schemas2or(cls, schemas):
#         def typechecked(data_tree_in, policy=None,):
#             for schema in schemas:
#                 try:
#                     DictschemaTool.tree2typechecked(
#                         data_tree_in, schema, policy=policy)
#                     return data_tree_in
#
#                 except (TypecheckFailError, TraverseFailError):
#                     continue
#         return typechecked
#
#     @classmethod
#     def schemas2and(cls, schemas):
#         def typechecked(data_tree_in, policy=None, ):
#             for schema in schemas:
#                 DictschemaTool.tree2typechecked(
#                     data_tree_in, schema, policy=policy)
#             return data_tree_in
#
#         return typechecked

class TypecheckFailError(Exception):
    pass


class DictschemaTool:

    @classmethod
    def jpath2get(cls, tree, schema, jpath):
        JsonTool.down_or_error(schema, jpath)
        return JsonTool.down(tree, jpath)

    @classmethod
    def tree2typechecked_terminal(cls, data, schema, policy=None):
        logger = FoxylibLogger.func_level2logger(
            cls.tree2typechecked_terminal, logging.DEBUG)

        logger.debug({'data': data, 'schema': schema})

        if schema is None:
            return data

        if TypingTool.is_annotation(schema):
            if TypingTool.is_instance(data, schema):
                return data

            raise TypecheckFailError({
                'schema': schema, 'data': data
            })

        if callable(schema):
            schema(data, policy=policy)
            return data

        raise ValueError({'schema': schema})

    @classmethod
    def schema2is_terminal(cls, schema):
        if schema is None:
            return True

        if isinstance(schema, (dict, list)):
            return False

        if TypingTool.is_annotation(schema):
            return True

        if IterTool.is_iterable(schema):
            raise NotImplementedError({'schema': schema})

        if callable(schema):
            return True

        return True

    @classmethod
    def tree2typechecked(cls, data_tree_in, schema_tree_in):
        logger = FoxylibLogger.func_level2logger(
            cls.tree2typechecked, logging.DEBUG)

        policy = DicttreeTool.Policy.FULL

        logger.debug({'data_tree_in': data_tree_in,
                      'schema_tree_in': schema_tree_in,
                      'policy':policy,
                      })

        if cls.schema2is_terminal(schema_tree_in):
            if not TypingTool.is_instance(data_tree_in, schema_tree_in):
                raise TypecheckFailError({
                    'data_tree_in': data_tree_in,
                    'schema_tree_in': schema_tree_in,
                })
            return data_tree_in

        if isinstance(schema_tree_in, (list, tuple, set,)):
            if not isinstance(data_tree_in, type(schema_tree_in)):
                raise TraverseFailError()

            schema_tree_this = l_singleton2obj(schema_tree_in)
            for x in data_tree_in:
                cls.tree2typechecked(x, schema_tree_this,)

            return data_tree_in

        if isinstance(schema_tree_in, (dict,)):
            keys_common = DicttreeTool.tree_pair2keys_common(
                data_tree_in, schema_tree_in, policy=policy)

            for k in keys_common:
                cls.tree2typechecked(data_tree_in[k], schema_tree_in[k],)

            return data_tree_in

        if callable(schema_tree_in):
            return schema_tree_in(data_tree_in,)

        logger.exception({'data_tree_in': data_tree_in,
                          'schema_tree_in': schema_tree_in,
                          })
        raise NotImplementedError()


    @classmethod
    def is_type_satisfied(cls, x_in, schema):
        try:
            v = cls.tree2typechecked(x_in, schema)
            assert_is(x_in, v)
            return True
        except (TypecheckFailError, TraverseFailError):
            return False

