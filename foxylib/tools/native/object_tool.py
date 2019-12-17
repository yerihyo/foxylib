class ObjectTool:
    @classmethod
    def obj2cls(cls, obj): return obj.__class__

obj2cls = ObjectTool.obj2cls