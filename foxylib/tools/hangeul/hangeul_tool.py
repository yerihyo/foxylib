from functools import reduce

from future.utils import lmap
from nose.tools import assert_equal


class HangeulTool:
    ORD_START = 0xAC00 # 44032
    ORD_END = 0xD7AF #55203

    ORD_JAMO_START = 0x1100  # 4352
    ORD_JAMO_END = 0x11FF  # 4352

    ORD_JAMO_COMPATIBILITY_START = 0x3131  # 4352

    CHOSEUNG_CYCLE = 588

    @classmethod
    def char2is_hangeul(cls, ch):
        assert_equal(len(ch), 1)

        o = ord(ch)

        if o < cls.ORD_START: return False
        if o > cls.ORD_END: return False
        return True

    @classmethod
    def char2is_jamo(cls, ch):
        o = ord(ch)

        if o < cls.ORD_JAMO_START: return False
        if o > cls.ORD_JAMO_END: return False
        return True


    @classmethod
    def _char2choseung(cls, ch):
        assert_equal(len(ch), 1)

        if not cls.char2is_hangeul(ch): return ch

        return chr((ord(ch) - cls.ORD_START) // cls.CHOSEUNG_CYCLE + cls.ORD_JAMO_START)

    @classmethod
    def str2choseung(cls, s):
        return "".join(lmap(cls._char2choseung, s))

    @classmethod
    def choseung2compatibility(cls, ch):
        if not cls.char2is_jamo(ch): return ch

        l = [0, 1, 3, 6, 7, 8, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        i = ord(ch) - cls.ORD_JAMO_START
        return chr(cls.ORD_JAMO_COMPATIBILITY_START + l[i])

    @classmethod
    def str2compatibility_choseung(cls, s):
        f_list = [cls.str2choseung, cls.choseung2compatibility]
        return "".join(lmap(lambda ch:reduce(lambda x,f:f(x), f_list, ch), s))
