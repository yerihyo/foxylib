class ObjectTool:
    @classmethod
    def obj2cls(cls, obj): return obj.__class__

    @classmethod
    def obj_name2has_variable(cls, obj, name):
        return name in obj.__dict__

    @classmethod
    def obj2dict(cls, obj):
        if hasattr(obj, "__slots__"):
            return cls.slotted2dict(obj)

        raise NotImplementedError()

    @classmethod
    def slotted2dict(cls, obj):
        return {s: getattr(obj, s) for s in obj.__slots__ if hasattr(obj, s)}

obj2cls = ObjectTool.obj2cls