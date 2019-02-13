class ClassToolkit:
    @classmethod
    def cls2name(cls, clazz): return clazz.__name__

    @classmethod
    def cls2name_lower(cls, clazz): return cls.cls2name(clazz).lower()
