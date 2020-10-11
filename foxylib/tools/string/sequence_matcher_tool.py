from difflib import SequenceMatcher

from future.utils import lfilter


class SequenceMatcherTool:
    @classmethod
    def list_pair2lcs_match(cls, s1, s2):
        # initialize SequenceMatcher object with
        # input string
        sm = SequenceMatcher(None, s1, s2)

        # find match of longest sub-string
        # output will be like Match(a=0, b=0, size=5)
        match = sm.find_longest_match(0, len(s1), 0, len(s2))

        if cls.match2is_empty(match):
            return None

        return match

    @classmethod
    # @PerformanceTool.profile_duration
    def list_pair2match_list(cls, s1, s2):
        # initialize SequenceMatcher object with
        # input string
        sm = SequenceMatcher(None, s1, s2)

        matches = sm.get_matching_blocks()

        return lfilter(lambda m: not cls.match2is_empty(m), matches)

    @classmethod
    # @PerformanceTool.profile_duration
    def match2span_a(cls, m):
        if cls.match2is_empty(m):
            return None

        return m.a, m.a + m.size

    @classmethod
    # @PerformanceTool.profile_duration
    def match2span_b(cls, m):
        if cls.match2is_empty(m):
            return None

        return m.b, m.b + m.size

    @classmethod
    # @PerformanceTool.profile_duration
    def match2span_pair(cls, m):
        return cls.match2span_a(m), cls.match2span_b(m)


    @classmethod
    def match2is_empty(cls, sm):
        if not sm:
            return True
        if not sm.size:
            return True
        return False
