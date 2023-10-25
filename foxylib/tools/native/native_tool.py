import logging
import math
from typing import Any, Optional

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class NoneTool:
    @classmethod
    def is_none(cls, x): return x is None

    @classmethod
    def is_not_none(cls, x: Any) -> bool:
        return x is not None

    @classmethod
    def is_all_none(cls, l):
        return all(map(cls.is_none, l))

    @classmethod
    def false2none(cls, x):
        return x if x else None

    @classmethod
    def v2default_if_none(cls, v, default):
        if v is None:
            return default

        return v


class BooleanTool:
    @classmethod
    def parse_sign2bool(cls, s):
        if s == "+": return True
        if s == "-": return False
        raise Exception("Invalid sign: {0}".format(s))

    @classmethod
    def parse2nullboolean(cls, s):
        logger = FoxylibLogger.func_level2logger(cls.parse2nullboolean, logging.DEBUG)
        logger.debug({"s":s})

        if any(map(lambda x: s is x, [None, True, False])):
            return s

        # logger.debug({"s": s, "s is False": s is False})

        if s is None:
            return None

        s_lower = s.lower()
        if s_lower.isdecimal():
            v = int(s_lower)
            return bool(v)

        if s_lower in {"true", "t", "yes", "y",}:
            return True

        if s_lower in {"false", "f", "no", "n", ""}:
            return False

        return None


class IntegerTool:
    @classmethod
    def parse_sign2int(cls, s):
        if not s:
            return 1

        if s == "+":
            return 1

        if s == "-":
            return -1

        raise Exception("Invalid sign: {0}".format(s))

    @classmethod
    def number2is_int(cls, v):
        if isinstance(v, int):
            return True

        if isinstance(v, float):
            return math.ceil(v) == v

        return False


class AttributeTool:
    @classmethod
    def get_or_lazyinit(cls, obj, attr, f_v):
        if hasattr(obj, attr):
            return getattr(obj, attr)

        v = f_v()
        setattr(obj, attr, v)
        return v

    @classmethod
    def get_or_init(cls, obj, attr, v):
        return cls.get_or_lazyinit(obj, attr, lambda: v)


def equal_type_and_value(v1, v2):
    if type(v1) != type(v2):
        return False

    return v1 == v2


is_none = NoneTool.is_none
is_not_none = NoneTool.is_not_none
is_all_none = NoneTool.is_all_none
