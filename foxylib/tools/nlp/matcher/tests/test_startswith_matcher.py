import logging
from unittest import TestCase

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.nlp.matcher.fulltext_matcher import FulltextMatcher
from foxylib.tools.nlp.matcher.startswith_matcher import StartswithMatcher
from foxylib.tools.string.string_tool import str2lower


class TestStartswithMatcher(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        dict_value2texts = {"ReD": ["scarleTT", "radish",]}

        matcher = StartswithMatcher(dict_value2texts, config=FulltextMatcher.Config(normalizer=str2lower))

        hyp1 = matcher.text2value("scarlett johansson")
        self.assertEqual(hyp1, "ReD")

        hyp2 = matcher.text2value("red scarlett johansson")
        self.assertIsNone(hyp2,)
