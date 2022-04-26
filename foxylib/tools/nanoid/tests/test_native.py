import logging
from unittest import TestCase

import pytest

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip("use case. not test")
    def test_1(self):
        # bash
        # echo "from nanoid import generate; [print(generate()) for i in range(32)]" | python
        pass
