import logging
from functools import partial
from pprint import pformat

from nose.tools import assert_is

from foxylib.tools.collections.collections_tool import merge_dicts, \
    f_vwrite2f_hvwrite, DictTool
from foxylib.tools.collections.dicttree.dicttree_tool import DicttreeTool
from foxylib.tools.collections.traversile.traversile_tool import TraversileTool, \
    TraverseFailError
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
#                     DicttreeTypecheckTool.tree2typechecked(
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
#                 DicttreeTypecheckTool.tree2typechecked(
#                     data_tree_in, schema, policy=policy)
#             return data_tree_in
#
#         return typechecked

class TypecheckFailError(Exception):
    pass


class DicttreeTypecheckTool:

    @classmethod
    def data_terminal2typechecked(cls, data, schema, policy=None):
        logger = FoxylibLogger.func_level2logger(
            cls.data_terminal2typechecked, logging.DEBUG)

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
    def tree2typechecked(cls, data_tree_in, schema_tree_in, policy=None, ):
        logger = FoxylibLogger.func_level2logger(
            cls.tree2typechecked, logging.DEBUG)

        # def schema2typechecker(schema):
        #     def typechecker(data, ):
        #         cls.data_terminal2typechecked(data, schema, policy=policy)
        #         return data
        #     return typechecker

        action_tree = TraversileTool.tree2traversed(
            schema_tree_in,
            lambda schema: partial(
                cls.data_terminal2typechecked, schema=schema, policy=policy)
        )

        logger.debug(pformat({
            'schema_tree_in':schema_tree_in,
            'action_tree':action_tree,
        }))

        DicttreeTool.tree2transduced(data_tree_in, action_tree, policy=policy)

        return data_tree_in

    @classmethod
    def converter2typechecked(cls, converter_tree, schema, ):
        data_tree = TraversileTool.tree2traversed(
            converter_tree,
            lambda x: None if callable(x) else x,
        )

        return cls.tree2typechecked(
            data_tree,
            schema,
            policy=DicttreeTool.Policy.PARTIAL_DATA,
        )

    @classmethod
    def is_type_satisfied(cls, x_in, schema, policy=None):
        try:
            v = cls.tree2typechecked(x_in, schema, policy=policy)
            assert_is(x_in, v)
            return True
        except (TypecheckFailError, TraverseFailError):
            return False

