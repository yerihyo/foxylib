class ArithmeticToolkit:
    @classmethod
    def divide_and_ceil(cls, v, d):
        q = v // d
        r = v % d
        return q + (1 if r else 0)