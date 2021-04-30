from decimal import Decimal
from typing import Union

from nose.tools import assert_true


class MathTool:
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
