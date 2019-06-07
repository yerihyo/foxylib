from future.utils import lmap
from nose.tools import assert_equal


class HangeulToolkit:
    CHOSUNG_START_LETTER = 4352
    JAMO_START_LETTER = 44032
    JAMO_END_LETTER = 55203
    JAMO_CYCLE = 588

    @classmethod
    def char2is_jamo(cls, ch):
        assert_equal(len(ch), 1)

        o = ord(ch)

        if o < cls.JAMO_START_LETTER: return False
        if o > cls.JAMO_END_LETTER: return False
        return True


    @classmethod
    def _jamo2choseung(cls, ch):
        assert_equal(len(ch), 1)

        if not cls.char2is_jamo(ch): return ch

        return chr((ord(ch) - cls.JAMO_START_LETTER) // cls.JAMO_CYCLE + cls.CHOSUNG_START_LETTER)

    @classmethod
    def str2choseng(cls, s):
        return "".join(lmap(cls._jamo2choseung, s))
