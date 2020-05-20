from foxylib.tools.function.function_tool import FunctionTool


class MethodTool:
    @classmethod
    def method2owner(cls, method):
        return method.__self__

    @classmethod
    def owner_function2method(cls, owner, function):
        return getattr(owner, FunctionTool.func2name(function))
