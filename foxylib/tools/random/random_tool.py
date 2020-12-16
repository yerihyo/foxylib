class RandomTool:
    @classmethod
    def lasvegas(cls, func, cond):
        while True:
            v = func()
            if cond(v):
                return v

        raise NotImplementedError("Should not arrive here!")
