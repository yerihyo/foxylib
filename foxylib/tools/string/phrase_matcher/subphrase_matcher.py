import logging
import sys
from functools import partial

from cachetools import LRUCache
from future.utils import lmap, lfilter

from foxylib.tools.cache.cache_manager import CacheManager
from foxylib.tools.collections.collections_tool import DictTool, merge_dicts
from foxylib.tools.function.warmer import Warmer
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.sequence_matcher_tool import SequenceMatcherTool
from foxylib.tools.string.string_tool import StringTool

MODULE = sys.modules[__name__]
WARMER = Warmer(MODULE)

logger = logging.getLogger(__name__)


class SubphraseMatch:
    class Field:
        FULLTEXT_REF = "fulltext_ref"
        TOKENS_REF = "tokens_ref"
        TOKENSPAN_REF = "tokenspan_ref"
        MATCHSTRING_REF = "matchstring_ref"
        CHARSPAN_REF = "charspan_ref"

        FULLTEXT_HYP = "fulltext_hyp"
        TOKENS_HYP = "tokens_hyp"
        TOKENSPAN_HYP = "tokenspan_hyp"
        MATCHSTRING_HYP = "matchstring_hyp"
        CHARSPAN_HYP = "charspan_hyp"

    @classmethod
    def norm(cls, match):
        keys = [cls.Field.CHARSPAN_REF,
                cls.Field.MATCHSTRING_REF,
                cls.Field.CHARSPAN_HYP,
                cls.Field.MATCHSTRING_HYP,
                ]
        return DictTool.exclude_keys(match, keys)

    @classmethod
    def match2fulltext_ref(cls, match):
        return match[cls.Field.FULLTEXT_REF]

    @classmethod
    def match2tokens_ref(cls, match):
        return match[cls.Field.TOKENS_REF]

    @classmethod
    def match2tokenspan_ref(cls, match):
        return match[cls.Field.TOKENSPAN_REF]

    @classmethod
    def match2charspan_ref(cls, match):
        """ lazy implementation """

        def _match2charspan_ref(_match):
            token_list_ref = cls.match2tokens_ref(_match)
            tokenspan_ref = cls.match2tokenspan_ref(_match)
            charspan_ref = SubphraseMatcher.Token.token_list_span2charspan(token_list_ref, tokenspan_ref)
            return charspan_ref

        return DictTool.lazyget(match, cls.Field.CHARSPAN_REF, partial(_match2charspan_ref, match))

    @classmethod
    # @VersionToolkit.inactive(msg="not used yet. expensive.")
    def match2matchstring_ref(cls, match):
        """ lazy implementation """

        def _match2matchstring_ref(_match):
            fulltext_ref = cls.match2fulltext_ref(_match)
            charspan_ref = cls.match2charspan_ref(_match)
            return StringTool.str_span2substr(fulltext_ref, charspan_ref)

        return DictTool.lazyget(match, cls.Field.MATCHSTRING_REF, partial(_match2matchstring_ref, match))

    @classmethod
    def match2fulltext_hyp(cls, match):
        return match[cls.Field.FULLTEXT_HYP]

    @classmethod
    def match2tokens_hyp(cls, match):
        return match[cls.Field.TOKENS_HYP]

    @classmethod
    def match2tokenspan_hyp(cls, match):
        return match[cls.Field.TOKENSPAN_HYP]

    @classmethod
    def match2charspan_hyp(cls, match):
        """ lazy implementation """

        def _match2charspan_hyp(_match):
            token_list_hyp = cls.match2tokens_hyp(_match)
            tokenspan_hyp = cls.match2tokenspan_hyp(_match)

            # logger.debug({"token_list_hyp":token_list_hyp, "tokenspan_hyp":tokenspan_hyp})

            charspan_hyp = SubphraseMatcher.Token.token_list_span2charspan(token_list_hyp, tokenspan_hyp)
            return charspan_hyp

        return DictTool.lazyget(match, cls.Field.CHARSPAN_HYP, partial(_match2charspan_hyp, match))

    @classmethod
    # @VersionToolkit.inactive(msg="not used yet. expensive.")
    def match2matchstring_hyp(cls, match):
        """ lazy implementation """

        def _match2matchstring_hyp(_match):
            fulltext_hyp = cls.match2fulltext_hyp(_match)
            charspan_hyp = cls.match2charspan_hyp(_match)
            return StringTool.str_span2substr(fulltext_hyp, charspan_hyp)

        return DictTool.lazyget(match, cls.Field.MATCHSTRING_HYP, partial(_match2matchstring_hyp, match))

    @classmethod
    def match2key(cls, match):
        charspan_ref = cls.match2charspan_ref(match)
        charspan_hyp = cls.match2charspan_hyp(match)
        tokens_hyp = cls.match2tokens_hyp(match)
        fulltext_hyp = cls.match2fulltext_hyp(match)

        key = (-SpanTool.span2len(cls.match2tokenspan_ref(match)),
               -SpanTool.span2len(charspan_hyp),
               -SpanTool.span2len(charspan_ref),
               len(tokens_hyp),
               len(fulltext_hyp),
               charspan_hyp,
               charspan_ref,
               )
        return key

    @classmethod
    def match_list2index_best(cls, match_list):
        if not match_list:
            return None

        n_match = len(match_list)
        return min(range(n_match), key=lambda i: cls.match2key(match_list[i]))

    @classmethod
    def match2has_equal_token_span_len(cls, _match):
        span_hyp = cls.match2tokenspan_ref(_match)
        span_ref = cls.match2tokenspan_hyp(_match)
        return SpanTool.span2len(span_hyp) == SpanTool.span2len(span_ref)

    @classmethod
    def match_list2perfects(cls, match_list):
        if not match_list:
            return None

        return lfilter(cls.match2has_equal_token_span_len, match_list)

    @classmethod
    def match_list2bests(cls, match_list):
        if not match_list:
            return []

        match_list_perfect = cls.match_list2perfects(match_list)
        if match_list_perfect:
            return match_list_perfect

        match_best = match_list[cls.match_list2index_best(match_list)]
        return [match_best]


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
            start, end = span

            s_token = token_list[start]
            e_token = token_list[end - 1]

            s_char = cls.token2span(s_token)[0]
            e_char = cls.token2span(e_token)[1]

            return s_char, e_char

    def __init__(self, config):
        self.config = config

    @classmethod
    def str2token_list(cls, str_in, spanizer, normalizer):
        span_list = spanizer(str_in)
        n_span = len(span_list)

        def index2token(index):
            span = span_list[index]
            text = StringTool.str_span2substr(str_in, span)

            token = {cls.Token.Field.INDEX: index,
                     cls.Token.Field.SPAN: span,
                     cls.Token.Field.TEXT: text,
                     cls.Token.Field.NORM: normalizer(text),
                     }
            return token

        token_list = lmap(index2token, range(n_span))
        return token_list

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1), )
    def token_list(self):
        cls = self.__class__

        reference = cls.Config.config2reference(self.config)
        spanizer = cls.Config.config2spanizer(self.config)
        normalizer = cls.Config.config2normalizer(self.config)

        return cls.str2token_list(reference, spanizer, normalizer)

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1), )
    def _dict_norm2index(self):
        cls = self.__class__

        token_list = self.token_list()

        h_out = merge_dicts([{cls.Token.token2norm(token): cls.Token.token2index(token)}
                             for token in token_list],
                            vwrite=DictTool.VWrite.skip_if_existing)
        return h_out

    def _norm2index(self, norm, default):
        return self._dict_norm2index().get(norm, default)

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1), )
    def index_list(self):
        cls = self.__class__
        return [self._norm2index(cls.Token.token2norm(token), i) for i, token in enumerate(self.token_list())]

    def tokens2sequence_match_list(self, token_list_hyp):
        cls = self.__class__

        indexes_list_ref = self.index_list()
        indexes_list_hyp = [self._norm2index(cls.Token.token2norm(token), -i) for i, token in
                            enumerate(token_list_hyp)]

        match_list = SequenceMatcherTool.list_pair2match_list(indexes_list_ref, indexes_list_hyp)
        return match_list

    @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=1), )
    def dict_norm2indexes(self):
        cls = self.__class__

        token_list = self.token_list()

        h_out = merge_dicts([{cls.Token.token2norm(token): {cls.Token.token2index(token)}}
                             for token in token_list],
                            vwrite=DictTool.VWrite.f_vresolve2f_vwrite(DictTool.VResolve.union))
        return h_out

    def norm2indexes(self, norm):
        return self.dict_norm2indexes().get(norm) or []

    def hyp2token_list(self, fulltext_hyp):
        cls = self.__class__

        spanizer = cls.Config.config2spanizer(self.config)
        normalizer = cls.Config.config2normalizer(self.config)

        token_list_hyp = cls.str2token_list(fulltext_hyp, spanizer, normalizer)
        return token_list_hyp

    @classmethod
    def str2match_list(cls, matcher, fulltext_hyp):
        fulltext_ref = SubphraseMatcher.Config.config2reference(matcher.config)

        token_list_ref = matcher.token_list()
        token_list_hyp = matcher.hyp2token_list(fulltext_hyp)

        word_list_ref = lmap(cls.Token.token2norm, token_list_ref)
        word_list_hyp = lmap(cls.Token.token2norm, token_list_hyp)

        sm_list = SequenceMatcherTool.list_pair2match_list(word_list_ref, word_list_hyp)

        def span_pair2match(span_ref, span_hyp):
            match = {SubphraseMatch.Field.FULLTEXT_REF: fulltext_ref,
                     SubphraseMatch.Field.TOKENS_REF: token_list_ref,
                     SubphraseMatch.Field.TOKENSPAN_REF: span_ref,
                     # SubphraseMatch.Field.CHARSPAN_REF: charspan_ref,

                     SubphraseMatch.Field.FULLTEXT_HYP: fulltext_hyp,
                     SubphraseMatch.Field.TOKENS_HYP: token_list_hyp,
                     SubphraseMatch.Field.TOKENSPAN_HYP: span_hyp,
                     # SubphraseMatch.Field.CHARSPAN_HYP: charspan_hyp,
                     }
            return match

        span_pair_list = lmap(SequenceMatcherTool.match2span_pair, sm_list)
        match_list = lmap(lambda p: span_pair2match(*p), span_pair_list)

        # raise Exception({"match_list":match_list})
        return match_list

    # class Approach:
    #     SEQUENCE_MATHCER = "sequence_matcher"

    @classmethod
    def str2match_bests(cls, matcher, text, ):
        match_list = cls.str2match_list(matcher, text, )
        return SubphraseMatch.match_list2bests(match_list)


