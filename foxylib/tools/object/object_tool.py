class ObjectTool:
    @classmethod
    def funcs2applied(cls, obj, funcs):
        for f in funcs:
            f(obj)

        return obj