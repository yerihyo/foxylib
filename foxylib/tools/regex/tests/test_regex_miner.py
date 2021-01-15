import logging
import os
import re
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_miner import RegexMiner
from foxylib.tools.regex.regex_tool import RegexTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

logger = logging.getLogger(__name__)


class TestRegexMiner(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        texts = ["abcd2343234",
                 "abcd2323435",
                 "abce2366465",
                 "abcd2398478",
                 ]
        hyp = RegexMiner.samelengths2regex(texts, thres_char_count=1)
        ref = 'abc[a-zA-Z]23\\d{5}'

        # pprint(hyp)

        self.assertEqual(hyp, ref)

        p = re.compile(RegexTool.rstr2wordbounded(hyp))
        logger.debug({'hyp':hyp, 'p':p})

        for text in texts:
            self.assertTrue(RegexTool.pattern_str2is_fullmatch(p, text))

    def test_02(self):
        hyp = list(RegexMiner.tokens2compressed(['5','2','\d','\d']))
        ref = ['5', '2', '\\d{2}']
        self.assertEqual(hyp, ref)

    def test_04(self):
        p = RegexMiner.pattern_stackable()
        # p = re.compile(RegexTool.rstr2rstr_words(rstr))

        self.assertIsNotNone(p.match("[0-9a-zA-Z]"))
        self.assertIsNotNone(p.match("[0-9a-z]"))
        self.assertIsNotNone(p.match("[a-z]"))

        self.assertIsNotNone(p.match("\\d"))
        self.assertIsNone(p.match("\\\\d"))


