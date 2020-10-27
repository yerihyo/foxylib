from nose.tools import assert_equal, assert_true


class NumberTool:
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

    @classmethod
    def sign(cls, n):
        if n > 0:
            return 1
        if n < 0:
            return -1
        return 0

    @classmethod
    def is_power_of_two(cls, n):
        return (n & (n-1) == 0) and n != 0

    @classmethod
    def int2log2(cls, n):
        assert_true(cls.is_power_of_two(n))

        return n.bit_length()-1
