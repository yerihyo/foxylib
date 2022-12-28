from decimal import Decimal
from functools import partial

from bson import Decimal128

from foxylib.tools.function.function_tool import FunctionTool


class DecimalTool:
    @classmethod
    def x2decimal(cls, x, ignore_unknown=False):
        if isinstance(x, (Decimal,)):
            return x

        if isinstance(x, (int,float,str)):
            return Decimal(x)

        if isinstance(x, (Decimal128,)):
            return Decimal(str(x))

        if ignore_unknown:
            return x

        raise NotImplementedError({'x': x})
