from nose.tools import assert_equal, assert_true


class NumberTool:

    @classmethod
    def x2float(cls, x):
        if x is None:
            return None

        if isinstance(x, (int,float)):
            return x

        if isinstance(x, (str,)):
            return float(x.replace(',', ''))

        raise NotImplementedError(f'x: {x}')

    @classmethod
    def x2int(cls, x):
        f = cls.x2float(x)
        return int(f) if f is not None else None

    @classmethod
    def index2order(cls, index):
        return index+1

    @classmethod
    def num2ordinal_suffix(cls, n):
        """
        reference: https://stackoverflow.com/a/20007730
        used // for int division
        """
        return "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]

    @classmethod
    def num2ordinal(cls, n):
        return "{}{}".format(n, cls.num2ordinal_suffix(n))

    # @classmethod
    # def sign(cls, n):
    #     if n > 0:
    #         return 1
    #     if n < 0:
    #         return -1
    #     if n == 0:
    #         return 0
    #
    #     raise NotImplementedError({'n':n})

    @classmethod
    def is_power_of_two(cls, n):
        return (n & (n-1) == 0) and n != 0

    @classmethod
    def int2log2(cls, n):
        assert_true(cls.is_power_of_two(n))

        return n.bit_length()-1

    @classmethod
    def int2log2_base(cls, n):
        return n.bit_length()-1

    @classmethod
    def int2log2_upper(cls, n):
        if cls.is_power_of_two(n):
            return n.bit_length() -1

        return n.bit_length()

    @classmethod
    def int2smallest_gte_power_of_two(cls, n):
        if cls.is_power_of_two(n):
            return n

        return 2**n.bit_length()

    @classmethod
    def int2largest_lte_power_of_two(cls, n):
        if cls.is_power_of_two(n):
            return n

        return 2 ** (n.bit_length()-1)


class SignTool:
    class Value:
        POSITIVE = POS = PLUS = 1
        NEGATIVE = NEG = MINUS = -1
        NEUTRAL = ZERO = 0

    @classmethod
    def symbol2sign(cls, s):
        if s == '+':
            return cls.Value.POS
        if s == '-':
            return cls.Value.NEG
        if s in {0, '0'}:
            return cls.Value.ZERO

        raise NotImplementedError({'s': s})
    @classmethod
    def sign(cls, v):
        if v > 0:
            return cls.Value.POS
        if v < 0:
            return cls.Value.NEG
        if v == 0:
            return cls.Value.ZERO

        raise NotImplementedError({'v': v})

