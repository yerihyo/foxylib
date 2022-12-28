import logging

from foxylib.tools.collections.collections_tool import l_singleton2obj, DictTool
from foxylib.tools.collections.traversile.traversile_tool import \
    TraverseFailError, TraversileTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class DicttreeTool:

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
    def tree2transduced(cls, data_tree_in, action_tree_in,):
        logger = FoxylibLogger.func_level2logger(
            cls.tree2transduced, logging.DEBUG)

        logger.debug({'data_tree_in':data_tree_in,
                      'action_tree_in':action_tree_in,
                      })

        if isinstance(action_tree_in, (list, tuple, set,)):
            if not isinstance(data_tree_in, type(action_tree_in)):
                raise TraverseFailError({
                    'data_tree_in': data_tree_in,
                    'action_tree_in': action_tree_in
                })

            action_tree_this = l_singleton2obj(action_tree_in)
            return [cls.tree2transduced(x, action_tree_this, )
                    for x in data_tree_in]

        # def kv2recursive(k, data_, action_):
        #     if isinstance(k, str):
        #         return {k: f_recursive(data_, action_)}
        #
        #     if callable(k):
        #         return k(v, policy=policy)

        if isinstance(action_tree_in, (dict,)):
            if not isinstance(data_tree_in, type(action_tree_in)):
                raise TraverseFailError({
                    'data_tree_in':data_tree_in,
                    'action_tree_in':action_tree_in
                })

            keys_common = set.union(
                set(data_tree_in.keys()),
                set(action_tree_in.keys())
            )

            return {k: cls.tree2transduced(data_tree_in[k], action_tree_in[k])
                    for k in keys_common}

        if callable(action_tree_in):
            return action_tree_in(data_tree_in,)

        logger.exception({'data_tree_in': data_tree_in,
                          'action_tree_in': action_tree_in,
                          })
        raise NotImplementedError()

    @classmethod
    def keys2removed(cls, dict_in, keys_exclusive):

        def node2keys_removed(dict_in_):
            if not isinstance(dict_in_, dict):
                return dict_in_

            h_tmp = DictTool.keys_excluded(dict_in_, keys_exclusive)

            return {k: cls.keys2removed(v, keys_exclusive)
                    for k, v in h_tmp.items()}

        dict_out = TraversileTool.tree2traversed(
            dict_in, node2keys_removed, target_types={list, set, tuple})
        return dict_out
