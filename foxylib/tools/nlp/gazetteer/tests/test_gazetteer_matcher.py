import logging
import re
from pprint import pprint
from unittest import TestCase

from future.utils import lmap

from linc_utils.entity_identification.entities.tool.gazetteer.gazetteer_matcher import GazetteerMatcher
from linc_utils.tools.regex.regex_tools import RegexToolkit
from linc_utils.tools.string.string_tools import str2lower


class TestGazetteerMatcher(TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

    def test_01(self):
        dict_value2texts = GazetteerMatcher.append_value2texts({"ReD": ["scarleTT", "radish"]})

        gazetteer = GazetteerMatcher(dict_value2texts, config={"normalizer":str2lower})
        span_value_list = gazetteer.text2span_value_list("red scarlett blue radish")


        hyp = span_value_list
        ref = [((0, 3), 'ReD'),
               ((4, 12), 'ReD'),
               ((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_02(self):
        dict_value2texts = {"ReD": ["scarleTT", "radish"]}

        gazetteer = GazetteerMatcher(dict_value2texts, config={"normalizer":str2lower})
        span_value_list = gazetteer.text2span_value_list("red scarlett blue radish")

        hyp = span_value_list
        ref = [((4, 12), 'ReD'), ((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_03(self):
        dict_value2texts = GazetteerMatcher.append_value2texts({"ReD": ["scarleTT", "radish"]})

        gazetteer = GazetteerMatcher(dict_value2texts)
        span_value_list = gazetteer.text2span_value_list("ReD scarlett blue radish")


        hyp = span_value_list
        ref = [((0, 3), 'ReD'), ((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_04(self):
        dict_value2texts = {"ReD": ["scarleTT", "radish"]}

        gazetteer = GazetteerMatcher(dict_value2texts)
        span_value_list = gazetteer.text2span_value_list("ReD scarlett blue radish")

        hyp = span_value_list
        ref = [((18, 24), 'ReD')]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    def test_05(self):
        gazetteer = {"black beauty": ["black"],
                     "black ugly": ["black"],
                     }

        gazetteer = GazetteerMatcher(gazetteer)
        span_value_list = gazetteer.text2span_value_list("black beauty ugly")

        hyp = set(span_value_list)
        ref = {((0, 5), 'black ugly'),
               ((0, 5), 'black beauty'),
               }

        # pprint(hyp)
        self.assertEqual(hyp, ref)




