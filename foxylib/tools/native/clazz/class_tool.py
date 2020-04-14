import inspect
from operator import itemgetter as ig

from future.utils import lfilter

from foxylib.tools.native.module.module_tool import ModuleTool


class ClassTool:
    @classmethod
    def cls2name(cls, clazz): return clazz.__name__

    @classmethod
    def cls2name_lower(cls, clazz): return cls.cls2name(clazz).lower()

    @classmethod
    def cls_name2has_variable(cls, clazz, name):
        return name in clazz.__dict__

    @classmethod
    def class2child_classes(cls, clazz):
        members = inspect.getmembers(clazz, inspect.isclass)
        children = lfilter(lambda x: x != type, map(ig(1), members))

        for child in children:
            yield child
            yield from ClassTool.class2child_classes(child)

    @classmethod
    def class2fullpath(cls, clazz):
        def class2module_qualname(clazz):
            return tuple([getattr(clazz, k) for k in ["__module__", "__qualname__"]])

        return ".".join(class2module_qualname(clazz))

cls2name = ClassTool.cls2name
