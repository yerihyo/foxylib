import itertools
import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        str_out = None

        def coro_x2oneadded():
            x = None
            try:
                for i in itertools.count():
                    if i != 0:
                        x += 1
                    x = yield x
            finally:
                nonlocal str_out
                str_out = "bye bye"

        def f():
            c = coro_x2oneadded()
            self.assertIs(c.send(None), None)
            self.assertEqual(c.send(1), 2)
            self.assertEqual(c.send(2), 3)

        f()
        self.assertEqual(str_out, "bye bye")  # exit safely
