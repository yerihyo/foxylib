from inspect import signature
from types import FunctionType

from nose.tools import assert_false, assert_not_equal, assert_true


class CallableTool:
    class Type:
        FUNCTION = "function"
        INSTANCEMETHOD = "instancemethod"
        CLASSMETHOD = "classmethod"

        # Impossible to detect if a function will become a classmethod from decorator's perspective
        #
        # INSTANCEMETHOD_BEFORE_DECORATOR = "instancemethod_before_decorator"
        # CLASSMETHOD_BEFORE_DECORATOR = "classmethod_before_decorator"

    @classmethod
    def callable2is_method(cls, callable_):
        t = cls.callable2type(callable_)
        return t in {cls.Type.INSTANCEMETHOD, cls.Type.CLASSMETHOD, } #cls.Type.CLASSMETHOD_BEFORE_DECORATOR}

    @classmethod
    def callable2type(cls, callable_):
        # is_function = isinstance(callable_, FunctionType)  # does not work for classmethod before decorator
        is_method = hasattr(callable_, "__self__")

        # raise Exception({"callable_":callable_,
        #                  "signature(callable).parameters": signature(callable_).parameters,
        #                  'hasattr(callable_, "__call__")':hasattr(callable_, "__call__"),
        #                  "isinstance(callable_, FunctionType)":isinstance(callable_, FunctionType),
        #                  # "method2owner": isinstance(callable_, FunctionType),
        #                  })

        if not is_method:
            assert_true(isinstance(callable_, FunctionType))
            return cls.Type.FUNCTION

        # if isinstance(callable_, FunctionType):
        #     return cls.Type.CLASSMETHOD_BEFORE_DECORATOR

        from foxylib.tools.function.method_tool import MethodTool
        if MethodTool.method2is_classmethod(callable_):
            return cls.Type.CLASSMETHOD
        else:
            return cls.Type.INSTANCEMETHOD

