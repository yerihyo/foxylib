from decimal import Decimal
from typing import Union

# from nose.tools import assert_true
from foxylib.asserts import assert_true


class MathTool:
    @classmethod
    def eqzero(cls, v: int) -> bool:
        return None if v is None else v == 0

    @classmethod
    def ltzero(cls, v:int) -> bool:
        return None if v is None else v < 0

    @classmethod
    def gtzero(cls, v: int) -> bool:
        return None if v is None else v > 0

    @classmethod
    def ltezero(cls, v: int) -> bool:
        return None if v is None else v <= 0

    @classmethod
    def gtezero(cls, v: int) -> bool:
        return None if v is None else v >= 0

    @classmethod
    def minus(cls, v1:int, v2:int):
        if v1 is None:
            return None
        if v2 is None:
            return None

        return v1 - v2

    @classmethod
    def whole_number2int(cls, x: Union[int, float]) -> int:
        if isinstance(x, int):
            return x

        if isinstance(x, float):
            assert_true(x.is_integer())
            return int(x)

        if isinstance(x, Decimal):
            assert_true(x % 1 == 0)
            return int(x)

        raise NotImplementedError(x)
