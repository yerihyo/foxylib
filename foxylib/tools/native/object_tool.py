class ObjectTool:
    @classmethod
    def obj2cls(cls, obj): return obj.__class__

    @classmethod
    def obj_name2has_variable(cls, obj, name):
        return name in obj.__dict__

obj2cls = ObjectTool.obj2cls