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
