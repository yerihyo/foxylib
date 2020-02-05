import inspect
import os
import sys
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

class ModuleTool:
    @classmethod
    def module2class_list(cls, module):
        m_list = inspect.getmembers(module, inspect.isclass)
        clazz_list = lfilter(lambda x:x.__module__ == module.__name__, map(ig(1), m_list))
        return clazz_list

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


cls2name = ClassTool.cls2name
module2class_list = ModuleTool.module2class_list