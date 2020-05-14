from unittest import TestCase

from foxylib.tools.bytes.bytes_tool import BytesTool


class TestBytesTool(TestCase):
    def test_01(self):
        bytes = b"abcde"
        hyp = BytesTool.bytes2utf8(bytes)
        ref = "abcde"

        self.assertEqual(hyp, ref)