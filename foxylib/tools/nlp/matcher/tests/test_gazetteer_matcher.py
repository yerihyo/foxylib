import logging
from unittest import TestCase

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.nlp.matcher.gazetteer_matcher import GazetteerMatcher
from foxylib.tools.string.string_tool import str2lower


class TestGazetteerMatcher(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        dict_value2texts = DictTool.append_key2values({"ReD": ["scarleTT", "radish"]})

        gazetteer = GazetteerMatcher(dict_value2texts, config={"normalizer":str2lower})
        span_value_list = list(gazetteer.text2span_value_iter("red scarlett blue radish"))

        hyp = span_value_list
        ref = [((0, 3), 'ReD'),
               ((4, 12), 'ReD'),
               ((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_02(self):
        dict_value2texts = {"ReD": ["scarleTT", "radish"]}

        gazetteer = GazetteerMatcher(dict_value2texts, config={"normalizer":str2lower})
        span_value_list = list(gazetteer.text2span_value_iter("red scarlett blue radish"))

        hyp = span_value_list
        ref = [((4, 12), 'ReD'), ((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_03(self):
        dict_value2texts = DictTool.append_key2values({"ReD": ["scarleTT", "radish"]})

        gazetteer = GazetteerMatcher(dict_value2texts)
        span_value_list = list(gazetteer.text2span_value_iter("ReD scarlett blue radish"))


        hyp = span_value_list
        ref = [((0, 3), 'ReD'), ((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_04(self):
        dict_value2texts = {"ReD": ["scarleTT", "radish"]}

        gazetteer = GazetteerMatcher(dict_value2texts)
        span_value_list = list(gazetteer.text2span_value_iter("ReD scarlett blue radish"))

        hyp = span_value_list
        ref = [((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_05(self):
        gazetteer = {"black beauty": ["black"],
                     "black ugly": ["black"],
                     }

        gazetteer = GazetteerMatcher(gazetteer)
        span_value_list = list(gazetteer.text2span_value_iter("black beauty ugly"))

        hyp = set(span_value_list)
        ref = {((0, 5), 'black ugly'),
               ((0, 5), 'black beauty'),
               }

        # pprint(hyp)
        self.assertEqual(hyp, ref)




