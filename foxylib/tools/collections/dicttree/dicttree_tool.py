import logging
from functools import partial, reduce
from pprint import pformat

from nose.tools import assert_true

from foxylib.tools.collections.collections_tool import l_singleton2obj, sfilter, \
    DictTool
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.collections.traversile.traversile_tool import \
    TraverseFailError, TraversileTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.json.jsonschema.jsonschema_tool import JsonschemaTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.typing.typing_tool import TypingTool


class DicttreeTool:
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
    def jpath2validated(cls, schema, jpath):
        JsonTool.down_or_error(schema, jpath)
        return jpath

    @classmethod
    def jpath2get(cls, j_in, schema, jpath):
        JsonschemaTool.jpath2checked(schema, jpath)
        return JsonTool.down(j_in, jpath)

    @classmethod
    def jpaths2filtered(cls, j_in, schema, jpaths):
        for jpath in jpaths:
            JsonTool.down_or_error(schema, jpath)

        j_out = JsonTool.jpaths2filtered(j_in, jpaths)
        return j_out

    @classmethod
    def jpath2filtered(cls, j_in, schema, jpath):
        return cls.jpaths2filtered(j_in, schema, [jpath])

    @classmethod
    def has_jpath(cls, j_in, schema, jpath):
        JsonTool.down_or_error(schema, jpath)
        return JsonTool.has_jpath(j_in, jpath)

    @classmethod
    def schema2keys_required(cls, schema):
        if not isinstance(schema, dict):
            raise ValueError({'schema':schema})

        for k,v in schema.items():
            if TypingTool.is_optional(v):
                continue

            yield k

    @classmethod
    def schema2is_terminal(cls, schema):
        if schema is None:
            return True

        if isinstance(schema, (dict, list)):
            return False

        if TypingTool.is_annotation(schema):
            return True

        if IterTool.is_iterable(schema):
            raise NotImplementedError({'schema':schema})

        if callable(schema):
            return True

        return True

    @classmethod
    def tree_pair2keys_common(cls, data_tree, action_tree, policy):
        logger = FoxylibLogger.func_level2logger(
            cls.tree_pair2keys_common, logging.DEBUG)

        assert_true(isinstance(action_tree, dict))

        if not isinstance(data_tree, dict):
            raise TraverseFailError()

        keys_data = set(data_tree.keys())
        keys_action = set(action_tree.keys())
        keys_action_req = set(cls.schema2keys_required(action_tree))

        logger.debug(pformat({
            'action_tree': action_tree,
            'keys_action_req': keys_action_req,
        }))

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

    # @classmethod
    # def tree2transduced_dict(cls, data_tree_in, action_tree_in, policy,):
    #     def keys_action_satisfy_data(data_tree_in_, action_tree_in_):
    #         keys_data = set(data_tree_in_.keys())
    #         keys_action_str = sfilter(lambda k: isinstance(k, str),
    #                                   action_tree_in_.keys())
    #         keys_data_remaining = keys_data - keys_action_str
    #
    #         node_classes = sfilter(lambda k: isinstance(k, str),
    #                                action_tree_in_.keys())
    #
    #         keys_unsatisfied = reduce(
    #             lambda keys, node: node.keys_data2unsatisfied(keys),
    #             node_classes,
    #             keys_data_remaining,
    #         )
    #
    #         if not keys_unsatisfied:
    #             return
    #
    #         raise ValueError({
    #             'data_tree_in_': data_tree_in_,
    #             'action_tree_in_': action_tree_in_,
    #             'keys_unsatisfied': keys_unsatisfied,
    #         })
    #
    #
    #     assert_true(isinstance(action_tree_in, dict))
    #
    #
    #
    #     keys_data = set(data_tree_in.keys())
    #     keys_action_str = sfilter(lambda k: isinstance(k, str),
    #                               action_tree_in.keys())

    @classmethod
    def tree2transduced(cls, data_tree_in, action_tree_in, policy=None, ):
        logger = FoxylibLogger.func_level2logger(
            cls.tree2transduced, logging.DEBUG)

        logger.debug({'data_tree_in':data_tree_in,
                      'action_tree_in':action_tree_in,
                      'policy':policy,
                      })

        policy = cls.Policy.policy2checked(policy) or cls.Policy.FULL
        f_recursive = partial(cls.tree2transduced, policy=policy)

        if isinstance(action_tree_in, (list, tuple, set,)):
            if not isinstance(data_tree_in, type(action_tree_in)):
                raise TraverseFailError()

            action_tree_this = l_singleton2obj(action_tree_in)
            return [f_recursive(x, action_tree_this, ) for x in data_tree_in]

        # def kv2recursive(k, data_, action_):
        #     if isinstance(k, str):
        #         return {k: f_recursive(data_, action_)}
        #
        #     if callable(k):
        #         return k(v, policy=policy)

        if isinstance(action_tree_in, (dict,)):
            keys_common = cls.tree_pair2keys_common(
                data_tree_in, action_tree_in, policy=policy)

            return {k: f_recursive(data_tree_in[k], action_tree_in[k])
                    for k in keys_common}

        if callable(action_tree_in):
            return action_tree_in(data_tree_in, policy=policy)

        logger.exception({'data_tree_in': data_tree_in,
                          'action_tree_in': action_tree_in,
                          })
        raise NotImplementedError()

    @classmethod
    def dicttree2keys_removed(cls, dict_in, keys_exclusive):

        def node2keys_removed(dict_in_):
            if not isinstance(dict_in_, dict):
                return dict_in_

            h_tmp = DictTool.keys_excluded(dict_in, keys_exclusive)

            return {k: cls.dicttree2keys_removed(v, keys_exclusive)
                    for k, v in h_tmp.items()}

        dict_out = TraversileTool.tree2traversed(
            dict_in, node2keys_removed, target_types={list, set, tuple})
        return dict_out
