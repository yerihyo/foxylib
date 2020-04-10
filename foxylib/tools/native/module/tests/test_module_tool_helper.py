import sys

MODULE = sys.modules[__name__]


class A:
    def a(self):
        pass

    class B:
        def b(self):
            pass

        class C:
            def c(self):
                pass
