import logging
from unittest import TestCase

from foxylib.tools.crypto.crypto_tool import CryptoTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestCryptoTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'A', 'alphabet': 'AB'},
                {'alphabet': 'CD', 'digit': 1},
            ),
            'C'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'B', 'alphabet': 'AB'},  # 1_2 = 1
                {'alphabet': 'CD', 'digit': 1},  # 1_2 = 1
            ),
            'D'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'B', 'alphabet': 'AB'},  # 1_2 = 1
                {'alphabet': 'CD', 'digit': 2},  # 1_2 = 01_2
            ),
            'CD'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'BAB', 'alphabet': 'AB'},  # 101_2 = 5
                {'alphabet': 'CD', 'digit': 2},  # 5%4 = 1 = 01_2
            ),
            'CD'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'BAB', 'alphabet': 'AB'},  # 101_2 = 5
                {'alphabet': 'CDE', 'digit': 2},  # 5 = 12_3
            ),
            'DE'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'ABAB', 'alphabet': 'AB'},  # 0101_2 = 5
                {'alphabet': 'CDE', 'digit': 2},  # 5 = 12_3
            ),
            'DE'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'BABA', 'alphabet': 'AB'},  # 1010_2 = 10
                {'alphabet': 'CDE', 'digit': 2},  # 10 % 9 = 1 = 01_3
            ),
            'CD'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': 'DCDA', 'alphabet': 'ABCDEF'},  # 3230_6 = 738
                {'alphabet': 'CDE', 'digit': 2},  # 738 % 9 = 0 = 00_3
            ),
            'CC'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': '45958487', 'alphabet': '0123456789'},
                {'alphabet': '01234567', 'digit': 4},  # 257242527_9
            ),
            '2527'
        )

        self.assertEqual(
            CryptoTool.ciphertext2rehashed(
                {'key': '45958487', 'alphabet': '0123456789'},
                {'alphabet': '012345678', 'digit': 5},  # 105427165_9
            ),
            '27165'
        )
