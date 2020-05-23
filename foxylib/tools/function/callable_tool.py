from types import FunctionType

from nose.tools import assert_false, assert_not_equal


class CallableTool:
    class Type:
        FUNCTION = "function"
        INSTANCEMETHOD = "instancemethod"
        CLASSMETHOD = "classmethod"
        CLASSMETHOD_BEFORE_DECORATOR = "classmethod_before_decorator"

    @classmethod
    def callable2is_method(cls, callable_):
        t = cls.callable2type(callable_)
        return t in {cls.Type.INSTANCEMETHOD, cls.Type.CLASSMETHOD, cls.Type.CLASSMETHOD_BEFORE_DECORATOR}

    @classmethod
    def callable2type(cls, callable_):
        # is_function = isinstance(callable_, FunctionType)  # does not work for classmethod before decorator
        is_method = hasattr(callable, "__self__")

        if not is_method:
            return cls.Type.FUNCTION

        if isinstance(callable_, FunctionType):
            return cls.Type.CLASSMETHOD_BEFORE_DECORATOR

        from foxylib.tools.function.method_tool import MethodTool
        if MethodTool.method2is_classmethod(callable_):
            return cls.Type.CLASSMETHOD
        else:
            return cls.Type.INSTANCEMETHOD

