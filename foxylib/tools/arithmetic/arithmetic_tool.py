class ArithmeticTool:
    @classmethod
    def divide_and_ceil(cls, v, d):
        q = v // d
        r = v % d
        return q + (1 if r else 0)

    @classmethod
    def modulo_d(cls, v, d):
        r = v % d
        if r == 0: return d
        return r