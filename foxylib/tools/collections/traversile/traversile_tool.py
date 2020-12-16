from functools import reduce, partial

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.json.json_typecheck_tool import JsonTypecheckTool


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
        def validate(cls, traversilities):
            if not cls.are_valid(traversilities):
                raise ValueError({'traversilities':traversilities})

        @classmethod
        def validates(cls, traversility):
            if not cls.is_valid(traversility):
                raise ValueError({'traversility': traversility})


    @classmethod
    def func2list_traversile(cls, func, target_types=None):
        if target_types is None:
            target_types = {list, set, tuple}

        def f_traversile(x):
            if isinstance(x, tuple(target_types), ):
                return type(x)([f_traversile(v) for v in x])

            return func(x)
        return f_traversile

    @classmethod
    def func2dict_traversile(cls, func, target_types=None):
        if target_types is None:
            target_types = {dict}

        def f_traversile(x):
            if isinstance(x, tuple(target_types),):
                return type(x)({k: f_traversile(v) for k, v in x.items()})

            return func(x)

        return f_traversile

    @classmethod
    def traversilities2wrapper(cls, traversilities):
        cls.Traversility.validate(traversilities)

        def traversilities2wrappers(traversility_set):
            if 'list' in traversility_set:
                yield cls.func2list_traversile

            if 'dict' in traversility_set:
                yield cls.func2dict_traversile

        wrappers = list(traversilities2wrappers(set(traversilities)))
        wrapper = FunctionTool.funcs2piped(wrappers)
        return wrapper

    @classmethod
    def func2traversiled(cls, func, traversilities):
        cls.Traversility.validate(traversilities)

        wrapper = cls.traversilities2wrapper(traversilities)
        return wrapper(func)
