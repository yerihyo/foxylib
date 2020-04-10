import inspect
from operator import itemgetter as ig

from future.utils import lfilter


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


cls2name = ClassTool.cls2name
