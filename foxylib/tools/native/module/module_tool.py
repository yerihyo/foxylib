import inspect
import os
import sys
from operator import itemgetter as ig


class ModuleTool:
    @classmethod
    def module2classes_within(cls, module):
        from foxylib.tools.native.clazz.class_tool import ClassTool

        member_list = inspect.getmembers(module, inspect.isclass)
        clazzes = filter(lambda x: x.__module__ == module.__name__, map(ig(1), member_list))

        for clazz in clazzes:
            yield from ClassTool.class2child_classes(clazz)
            yield clazz

    @classmethod
    def get_module(cls, x):
        try:
            return getattr(x, '__module__')
        except AttributeError:
            return None

    @classmethod
    def x2filepath(cls, x):
        module = cls.get_module(x)
        if module is None:
            return None

        return os.path.abspath(sys.modules[module].__file__)

    @classmethod
    def class2filepath(cls, clazz):
        return cls.x2filepath(clazz)

    @classmethod
    def func2filepath(cls, func):
        return cls.x2filepath(func)


