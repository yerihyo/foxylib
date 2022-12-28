import logging
import re
import sys
from functools import lru_cache, partial, reduce
from itertools import chain
from string import punctuation

from cachetools import cachedmethod, LRUCache
from nose.tools import assert_true

from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.collections.collections_tool import sfilter, merge_dicts, vwrite_no_duplicate_key, DictTool
from future.utils import lmap, lfilter

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import AttributeTool
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.string_tool import StringTool, str2lower


class Cospan:
    class Field:
        SPAN_REF = "span_ref"
        SPAN_HYP = "span_hyp"

    @classmethod
    def cospan2span_ref(cls, cospan):
        return cospan[cls.Field.SPAN_REF]

    @classmethod
    def cospan2span_hyp(cls, cospan):
        return cospan[cls.Field.SPAN_HYP]

    @classmethod
    def cospan2inc(cls, cospan):
        return {cls.Field.SPAN_REF: SpanTool.span2inc(cls.cospan2span_ref(cospan)),
                cls.Field.SPAN_HYP: SpanTool.span2inc(cls.cospan2span_hyp(cospan)),
                }

    @classmethod
    def i_pair2cospan_unit(cls, i_ref, i_hyp):
        return {cls.Field.SPAN_REF: (i_ref, i_ref+1),
                cls.Field.SPAN_HYP: (i_hyp, i_hyp+1),
                }

    @classmethod
    def ref_indexes_list2cospans(cls, ref_indexes_list):
        logger = FoxylibLogger.func_level2logger(cls.ref_indexes_list2cospans, logging.DEBUG)

        # n = len(indexes_list)
        def cospan2i_ref2cospan(cospan):
            return {cls.cospan2span_ref(cospan)[1]: cospan}

        h_i_ref2cospan_ontable = {}
        for i_hyp, indexes_ref in enumerate(ref_indexes_list):

            # logger.debug({"h_i_ref2cospan_ontable":h_i_ref2cospan_ontable})
            # p = len(span_pairs_on_table)
            # q = len(indexes_ref)

            indexes_ref_ontable = sfilter(lambda i_ref: i_ref in h_i_ref2cospan_ontable, indexes_ref)
            indexes_ref_offtable = sfilter(lambda i_ref: i_ref not in indexes_ref_ontable, indexes_ref)

            cospans_discontinued = [cospan
                                       for i_ref, cospan in h_i_ref2cospan_ontable.items()
                                       if i_ref not in indexes_ref_ontable
                                       ]
            yield from cospans_discontinued

            cospan_ontable = [cls.cospan2inc(h_i_ref2cospan_ontable[i_ref])
                              for i_ref in indexes_ref_ontable]
            cospan_offtable = [cls.i_pair2cospan_unit(i_ref, i_hyp)
                              for i_ref in indexes_ref_offtable]

            h_i_ref2cospan_ontable = merge_dicts(lmap(cospan2i_ref2cospan, chain(cospan_ontable, cospan_offtable)),
                                                 vwrite=vwrite_no_duplicate_key)

            logger.debug({
                "i_hyp": i_hyp,
                "h_i_ref2cospan_ontable": h_i_ref2cospan_ontable,
                "cospans_discontinued":cospans_discontinued,
                "indexes_ref_ontable":indexes_ref_ontable,
                "indexes_ref_offtable":indexes_ref_offtable,
            })

        yield from h_i_ref2cospan_ontable.values()


class SubphraseMatch:
    class Field:
        TEXT_REF = "text_ref"
        TOKENSPAN_REF = "tokenspan_ref"
        CHARSPAN_REF = "charspan_ref"

        TEXT_HYP = "text_hyp"
        TOKENSPAN_HYP = "tokenspan_hyp"
        CHARSPAN_HYP = "charspan_hyp"

    @classmethod
    def match2text_ref(cls, match):
        return match[cls.Field.TEXT_REF]

    @classmethod
    def match2tokenspan_ref(cls, match):
        return match[cls.Field.TOKENSPAN_REF]

    @classmethod
    def match2charspan_ref(cls, match):
        return match[cls.Field.CHARSPAN_REF]

    @classmethod
    def match2text_hyp(cls, match):
        return match[cls.Field.TEXT_HYP]

    @classmethod
    def match2tokenspan_hyp(cls, match):
        return match[cls.Field.TOKENSPAN_HYP]

    @classmethod
    def match2charspan_hyp(cls, match):
        return match[cls.Field.CHARSPAN_HYP]

    @classmethod
    def match2key(cls, match):
        charspan_ref = cls.match2charspan_ref(match)
        charspan_hyp = cls.match2charspan_hyp(match)

        key = (-SpanTool.span2len(cls.match2tokenspan_ref(match)),
               -SpanTool.span2len(charspan_hyp),
               -SpanTool.span2len(charspan_ref),
               charspan_hyp,
               charspan_ref,
               )
        return key

    @classmethod
    def match_list2index_best(cls, match_list):
        n = len(match_list)
        return min(range(n), key=lambda i: cls.match2key(match_list[i]))

    @classmethod
    def match_list2best(cls, match_list):
        return match_list[cls.match_list2index_best(match_list)]


class SubphraseMatcher:
    class Config:
        REFERENCE = "reference"
        SPANIZER = "spanizer"
        NORMALIZER = "normalizer"

        @classmethod
        def config2reference(cls, config):
            return config[cls.REFERENCE]

        @classmethod
        def config2spanizer(cls, config):
            return config.get(cls.SPANIZER)

        @classmethod
        def config2normalizer(cls, config):
            return config[cls.NORMALIZER]

    class Token:
        class Field:
            INDEX = "index"
            SPAN = "span"
            TEXT = "text"
            NORM = "norm"

        @classmethod
        def token2index(cls, token):
            return token[cls.Field.INDEX]

        @classmethod
        def token2span(cls, token):
            return token[cls.Field.SPAN]

        @classmethod
        def token2text(cls, token):
            return token[cls.Field.TEXT]

        @classmethod
        def token2norm(cls, token):
            return token[cls.Field.NORM]

        @classmethod
        def token_list_span2charspan(cls, token_list, span):
            s,e = span
            return (cls.token2span(token_list[s])[0],
                    cls.token2span(token_list[e - 1])[1],
                    )


    def __init__(self, config):
        self.config = config

    @classmethod
    def str2token_list(cls, str_in, spanizer, normalizer):
        assert_true(spanizer)

        span_list = spanizer(str_in)
        n = len(span_list)

        def index2token(index):
            span = span_list[index]
            text = StringTool.str_span2substr(str_in, span)

            token = {cls.Token.Field.INDEX: index,
                     cls.Token.Field.SPAN: span,
                     cls.Token.Field.TEXT: text,
                     cls.Token.Field.NORM: normalizer(text) if normalizer else text,
                     }
            return token

        token_list = lmap(index2token, range(n))
        return token_list

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1))
    def token_list(self):
        cls = self.__class__

        reference = cls.Config.config2reference(self.config)
        spanizer = cls.Config.config2spanizer(self.config)
        normalizer = cls.Config.config2normalizer(self.config)

        return cls.str2token_list(reference, spanizer, normalizer)

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1))
    def dict_norm2indexes(self):
        cls = self.__class__

        token_list = self.token_list()

        h = merge_dicts([{cls.Token.token2norm(token): {cls.Token.token2index(token)}}
                         for token in token_list],
                        vwrite=DictTool.VWrite.f_vresolve2f_vwrite(DictTool.VResolve.union))
        return h

    def norm2indexes(self, norm):
        return self.dict_norm2indexes().get(norm) or []

    def tokens2cospan_list(self, token_list):
        cls = self.__class__
        indexes_list = lmap(lambda token: self.norm2indexes(cls.Token.token2norm(token)), token_list)
        cospan_list = list(Cospan.ref_indexes_list2cospans(indexes_list))
        return cospan_list

    @classmethod
    def cospan2key(cls, cospan, token_list_ref, token_list_hyp):
        span_ref = Cospan.cospan2span_ref(cospan)
        charspan_ref = cls.Token.token_list_span2charspan(token_list_ref, span_ref)

        span_hyp = Cospan.cospan2span_hyp(cospan)
        charspan_hyp = cls.Token.token_list_span2charspan(token_list_hyp, span_hyp)

        key = (-SpanTool.span2len(span_ref),
               -SpanTool.span2len(charspan_hyp),
               -SpanTool.span2len(charspan_ref),
               charspan_hyp,
               charspan_ref,
               )
        return key


    @classmethod
    def str2match_list(cls, matcher, text):
        spanizer = cls.Config.config2spanizer(matcher.config)
        normalizer = cls.Config.config2normalizer(matcher.config)

        token_list_ref = matcher.token_list()
        token_list_hyp = cls.str2token_list(text, spanizer, normalizer)

        cospan_list = matcher.tokens2cospan_list(token_list_hyp)

        def cospan2match(cospan):
            span_ref = Cospan.cospan2span_ref(cospan)
            charspan_ref = cls.Token.token_list_span2charspan(token_list_ref, span_ref)
            text_ref = StringTool.str_span2substr(cls.Config.config2reference(matcher.config), charspan_ref)

            span_hyp = Cospan.cospan2span_hyp(cospan)
            charspan_hyp = cls.Token.token_list_span2charspan(token_list_hyp, span_hyp)
            text_hyp = StringTool.str_span2substr(text, charspan_hyp)

            match = {SubphraseMatch.Field.TOKENSPAN_REF: span_ref,
                     SubphraseMatch.Field.CHARSPAN_REF: charspan_ref,
                     SubphraseMatch.Field.TEXT_REF: text_ref,

                     SubphraseMatch.Field.TOKENSPAN_HYP: span_hyp,
                     SubphraseMatch.Field.CHARSPAN_HYP: charspan_hyp,
                     SubphraseMatch.Field.TEXT_HYP: text_hyp,
                     }
            return match

        match_list = lmap(cospan2match, cospan_list)
        return match_list

    @classmethod
    def str2match_best(cls, matcher, text):
        match_list = cls.str2match_list(matcher, text)
        return SubphraseMatch.match_list2best(match_list)


class EnglishSubphraseMatcher:
    @classmethod
    def normalizer(cls, str_in):
        func_list = [lambda s: s.rstr(punctuation).strip(),
                     lambda s: s.rstrip("s").strip(),
                     str2lower,
                     ]

        str_out = reduce(lambda x,f:f(x), func_list, str_in)
        return str_out

    @classmethod
    def text2matcher(cls, text):
        from foxylib.tools.nlp.tokenizer.en.simple_tokenizer import EnglishSimpleTokenizer

        config = {SubphraseMatcher.Config.REFERENCE:text,
                  SubphraseMatcher.Config.SPANIZER: EnglishSimpleTokenizer.str2token_span_list,
                  SubphraseMatcher.Config.NORMALIZER: cls.normalizer,
                  }
        matcher = SubphraseMatcher(config)
        return matcher

