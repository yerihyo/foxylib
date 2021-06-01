import re
import sys
from functools import lru_cache

from foxylib.tools.regex.regex_tool import RegexTool


class ArgvTool:
    @classmethod
    @lru_cache(maxsize=2)
    def pattern_delim(cls):
        return re.compile(RegexTool.rstrs2or(['\s+', '/']))

    @classmethod
    def argv2is_pytest(cls, argv):
        def argv2tokens(argv_):
            for str_arg in argv_:
                tokens = cls.pattern_delim().split(str_arg.strip().lower())
                # raise Exception({'tokens':tokens})
                for token in tokens:
                    yield token

        for token in argv2tokens(argv):
            if "pytest" in token:
                return True

        return False

    @classmethod
    def argv2is_unittest(cls, argv):
        for arg in argv:
            # pycharm
            if argv[0].endswith("/_jb_unittest_runner.py"):
                return True

            for token in arg.strip().lower().split():
                if token in {"unittest"}:
                    return True

        return False

    @classmethod
    def argv2is_test(cls, argv):
        if cls.argv2is_pytest(argv):
            return True

        if cls.argv2is_unittest(argv):
            return True

        return False
