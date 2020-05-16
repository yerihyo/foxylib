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
    def x2module(cls, x):
        return x.__module__

    @classmethod
    def x2filepath(cls, x):
        return os.path.abspath(sys.modules[x.__module__].__file__)

    @classmethod
    def class2filepath(cls, clazz):
        return cls.x2filepath(clazz)

    @classmethod
    def func2filepath(cls, func):
        return cls.x2filepath(func)


