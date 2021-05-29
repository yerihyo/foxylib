import sys


class ArgvTool:
    @classmethod
    def is_within_pytest(cls):
        in_pytest = any("pytest" in s.strip().lower().split() for s in sys.argv)
        # in_pytest = os.path.basename(sys.argv[0]) in ('pytest', 'py.test')
        return in_pytest

    @classmethod
    def is_within_unittest(cls):
        in_unittest = any("unittest" in s.strip().lower().split() for s in sys.argv)
        return in_unittest

    @classmethod
    def is_within_test(cls):
        if cls.is_within_pytest():
            return True

        if cls.is_within_unittest():
            return True

        return False
