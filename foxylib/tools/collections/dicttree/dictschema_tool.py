import logging
from pprint import pformat

from nose.tools import assert_is, assert_true

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

class SchemaValue:
    class Optional:
        def __init__(self, subtree):
            self.subtree = subtree

        def typechecked(self, data_in):
            if not data_in:
                return data_in

            return DictschemaTool.tree2typechecked(data_in, self.subtree)

    @classmethod
    def values(cls):
        return {cls.Optional}


class TypecheckFailError(Exception):
    pass


class DictschemaTool:
    class Policy:
        FULL = 'full'
        PARTIAL_SCHEMA = 'partial_schema'
        PARTIAL_DATA = 'partial_data',
        EXISTING_KEYS_ONLY = 'existing_keys_only'

        @classmethod
        def values(cls):
            return {
                cls.FULL, cls.PARTIAL_SCHEMA,
                cls.PARTIAL_DATA, cls.EXISTING_KEYS_ONLY
            }

        @classmethod
        def policy2checked(cls, v):
            if v is None:
                return None

            if v not in cls.values():
                raise NotImplementedError({'policy':v})

            return v

        @classmethod
        def is_partial_data_allowed(cls, policy_in):
            cls.policy2checked(policy_in)

            return policy_in in {cls.PARTIAL_DATA, cls.EXISTING_KEYS_ONLY}

        @classmethod
        def is_partial_schema_allowed(cls, policy_in):
            cls.policy2checked(policy_in)

            return policy_in in {cls.PARTIAL_SCHEMA, cls.EXISTING_KEYS_ONLY}

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
    def tree2typechecked(cls, data_tree_in, schema_tree_in,):
        logger = FoxylibLogger.func_level2logger(
            cls.tree2typechecked, logging.DEBUG)

        policy = cls.Policy.FULL

        # logger.debug({'data_tree_in': data_tree_in,
        #               'schema_tree_in': schema_tree_in,
        #               'policy':policy,
        #               })

        if isinstance(schema_tree_in, tuple(SchemaValue.values())):
            schema_tree_in.typechecked(data_tree_in)
            return data_tree_in

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
            keys_common = cls.tree_pair2keys_common(
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

    @classmethod
    def schema2keys_required(cls, schema):
        if not isinstance(schema, dict):
            raise ValueError({'schema': schema})

        for k, v in schema.items():
            if TypingTool.is_optional(v):
                continue

            if isinstance(v, SchemaValue.Optional):
                continue

            yield k

    @classmethod
    def tree_pair2keys_common(cls, data_tree, action_tree, policy):
        logger = FoxylibLogger.func_level2logger(
            cls.tree_pair2keys_common, logging.DEBUG)

        if not isinstance(action_tree, dict):
            raise ValueError({'action_tree':action_tree})

        if not isinstance(data_tree, dict):
            raise TraverseFailError()

        keys_data = set(data_tree.keys())
        keys_action = set(action_tree.keys())
        keys_action_req = set(cls.schema2keys_required(action_tree))

        # logger.debug(pformat({
        #     'action_tree': action_tree,
        #     'keys_action_req': keys_action_req,
        # }))

        if not cls.Policy.is_partial_schema_allowed(policy):
            if keys_data - keys_action:
                context = {
                    'data_tree': data_tree,
                    'action_tree': action_tree,
                    'keys_data': keys_data,
                    'keys_action': keys_action
                }
                logger.exception(pformat(context))
                raise TraverseFailError(context)

        if not cls.Policy.is_partial_data_allowed(policy):
            if keys_action_req - keys_data:
                context = {
                    'data_tree': data_tree,
                    'action_tree': action_tree,
                    'keys_data': keys_data,
                    'keys_action_req': keys_action_req
                }
                logger.exception(pformat(context))
                raise TraverseFailError(context)

        keys_common = keys_data & keys_action_req
        return keys_common