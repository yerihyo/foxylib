import logging
from pprint import pformat

from foxylib.tools.collections.collections_tool import schain
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TraverseFailError(Exception):
    pass


class TraversileTool:
    class Traversility:
        # DICT = 'dict'
        # LIST = 'list'

        @classmethod
        def values(cls):
            return {'list','dict'}

        @classmethod
        def are_valid(cls, traversilities):
            return set(traversilities) <= cls.values()

        @classmethod
        def is_valid(cls, traversility):
            return cls.are_valid({traversility})

        @classmethod
        def typechecked(cls, traversilities):
            if not cls.are_valid(traversilities):
                raise ValueError({'traversilities':traversilities})


    # @classmethod
    # def func2list_traversile(cls, func, target_types=None):
    #     logger = FoxylibLogger.func_level2logger(
    #         cls.func2list_traversile, logging.DEBUG)
    #
    #     if target_types is None:
    #         target_types = {list, set, tuple}
    #
    #     def f_traversile(x):
    #         logger.debug({'x':x})
    #
    #         if isinstance(x, tuple(target_types), ):
    #             return type(x)([f_traversile(v) for v in x])
    #
    #         return func(x)
    #     return f_traversile
    #
    # @classmethod
    # def func2dict_traversile(cls, func, target_types=None):
    #     logger = FoxylibLogger.func_level2logger(
    #         cls.func2dict_traversile, logging.DEBUG)
    #
    #     if target_types is None:
    #         target_types = {dict}
    #
    #     def f_traversile(x):
    #         logger.debug({'x': x})
    #
    #         if isinstance(x, tuple(target_types),):
    #             return type(x)({k: f_traversile(v)
    #                             for k, v in x.items()})
    #
    #         return func(x)
    #
    #     return f_traversile

    @classmethod
    def traversilities2target_types(cls, traversilities):
        h = {'list': {list, set, tuple},
             'dict': {dict},
             }

        return schain(*[h[traversility] for traversility in traversilities])

    @classmethod
    def func2traversile(cls, func, target_types=None):
        # logger = FoxylibLogger.func_level2logger(
        #     cls.func2traversile, logging.DEBUG)

        if target_types is None:
            target_types = {dict, list, set, tuple}

        def traversiled(x):
            # logger.debug({'x': x})

            if isinstance(x, tuple(set(target_types) & {dict}),):
                h = type(x)({k: traversiled(v)
                                for k, v in x.items()})
                return h

            if isinstance(x, tuple(set(target_types) & {list, set, tuple}), ):
                # logger.debug(pformat({'x':x}))
                l = type(x)([traversiled(v) for v in x])
                return l

            return func(x)

        return traversiled

    # @classmethod
    # def traversilities2wrapper(cls, traversilities):
    #     cls.Traversility.typechecked(traversilities)
    #
    #     def traversilities2wrappers(traversility_set):
    #         if 'list' in traversility_set:
    #             yield cls.func2list_traversile
    #
    #         if 'dict' in traversility_set:
    #             yield cls.func2dict_traversile
    #
    #     wrappers = list(traversilities2wrappers(set(traversilities)))
    #     wrapper = FunctionTool.funcs2piped(wrappers)
    #     return wrapper
    #
    # @classmethod
    # def func2traversiled(cls, func, traversilities=None):
    #     if traversilities is None:
    #         traversilities = cls.Traversility.values()
    #
    #     cls.Traversility.typechecked(traversilities)
    #
    #     wrapper = cls.traversilities2wrapper(traversilities)
    #     return wrapper(func)

    @classmethod
    def tree2traversed(cls, tree_in, func, target_types=None):
        f_traversile = cls.func2traversile(func, target_types=target_types)
        tree_out = f_traversile(tree_in)
        return tree_out
