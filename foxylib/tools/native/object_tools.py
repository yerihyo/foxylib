class ObjectToolkit:
    @classmethod
    def obj2cls(cls, obj): return obj.__class__

obj2cls = ObjectToolkit.obj2cls