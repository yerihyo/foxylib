import logging
from unittest import TestCase

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.nlp.matcher.fulltext_matcher import FulltextMatcher
from foxylib.tools.string.string_tool import str2lower


class TestFulltextMatcher(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        dict_value2texts = DictTool.append_key2values({"ReD": ["scarleTT", "radish"]})

        matcher = FulltextMatcher(dict_value2texts, config=FulltextMatcher.Config(normalizer=str2lower))

        hyp1 = list(matcher.text2values("scarlett"))
        self.assertEqual(hyp1, ["ReD"])

        hyp2 = list(matcher.text2values("red scarlett"))
        self.assertEqual(hyp2, [])
