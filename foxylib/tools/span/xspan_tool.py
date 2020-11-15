from operator import itemgetter as ig

from foxylib.tools.collections.collections_tool import AbsoluteOrder
from future.utils import lmap
from nose.tools import assert_equal, assert_false


class XspanTool:
    class Constant:
        INF = None

    class Clusivity:
        IN = True
        EX = False

    class Policy:
        INEX = "inex"
        ININ = "inin"
        EXEX = "exex"
        EXIN = "exin"

        @classmethod
        def policy2clusivities(cls, policy):
            return (policy in {cls.ININ, cls.INEX},
                    policy in {cls.ININ, cls.EXIN}
                    )

    @classmethod
    def value2is_inf(cls, value):
        return value is cls.Constant.INF

    @classmethod
    def xspan2bool(cls, xspan):
        return cls.xspan2has_span(xspan)

    @classmethod
    def xspan2has_span(cls, xspan):
        if not xspan:
            return False

        (s,s_inex), (e,e_inex) = xspan

        if cls.value2is_inf(s):
            assert_false(s_inex)
            return True

        if cls.value2is_inf(e):
            assert_false(e_inex)
            return True

        if s < e:
            return True

        if s > e:
            return False

        assert_equal(s, e)
        return s_inex and e_inex

        # if s_inex and e_inex:
        #     return True
        #
        # return False

    @classmethod
    def xvalue2is_inclusive(cls, xvalue):
        return xvalue[1]

    @classmethod
    def xspan2clusivities(cls, xspan):
        return lmap(ig(1), xspan)

    @classmethod
    def xspan2len(cls, xspan):
        return cls.xspan2end(xspan) - cls.xspan2start(xspan)

    @classmethod
    def xstarts2max(cls, xstarts):
        s = max(lmap(ig(0), xstarts), key=AbsoluteOrder.null2min)
        inex = all(map(ig(1), filter(lambda x:x[0]==s, xstarts)))
        return s, inex

    @classmethod
    def xends2min(cls, xends):
        e = min(lmap(ig(0), xends), key=AbsoluteOrder.null2max)
        inex = all(map(ig(1), filter(lambda x: x[0] == e, xends)))
        return e, inex

    @classmethod
    def intersect(cls, xspan1, xspan2):
        xstart1, xend1 = xspan1
        xstart2, xend2 = xspan2

        xstart = cls.xstarts2max([xstart1, xstart2])
        xend = cls.xends2min([xend1, xend2])
        xspan = xstart, xend

        if not cls.xspan2has_span(xspan):
            return None

        return xspan

    @classmethod
    def overlaps(cls, xspan1, xspan2):
        xspan = cls.intersect(xspan1, xspan2)
        return xspan is not None

    @classmethod
    def xstart2has_started(cls, xstart, value_pivot):
        s, s_inex = xstart
        if cls.value2is_inf(s):
            return True

        if s < value_pivot:
            return True

        if s > value_pivot:
            return False

        assert_equal(s, value_pivot)
        return cls.xvalue2is_inclusive(xstart)

    @classmethod
    def xend2has_ended(cls, xend, value_pivot):
        e, e_inex = xend
        if cls.value2is_inf(e):
            return False

        if e < value_pivot:
            return True

        if e > value_pivot:
            return False

        assert_equal(e, value_pivot)
        return not cls.xvalue2is_inclusive(xend)

    @classmethod
    def is_in(cls, v, xspan):
        xstart, xend = xspan

        has_started = cls.xstart2has_started(xstart, v)
        if not has_started:
            return False

        has_ended = cls.xend2has_ended(xend, v)
        if has_ended:
            return False

        return True


    @classmethod
    def xspan2key_sort(cls, xspan):
        (s, s_inex), (e, e_inex) = xspan

        k = (s,
             -1 if s_inex else 0,
             e,
             1 if e_inex else 0,
             )

        return k


    @classmethod
    def xspan2start(cls, xspan):
        return cls.xvalue2value(xspan[0])

    @classmethod
    def xspan2end(cls, xspan):
        return cls.xvalue2value(xspan[1])

    @classmethod
    def xvalue2value(cls, xvalue):
        value, clusivity = xvalue
        return value

    @classmethod
    def xspan2span(cls, xspan):
        return lmap(cls.xvalue2value, xspan)

    @classmethod
    def value2xvalue(cls, v, clusivity):
        if v is None:
            return v, cls.Clusivity.EX

        return v, clusivity

    @classmethod
    def span2xspan(cls, span, policy):
        start, end = span

        clusivities = cls.Policy.policy2clusivities(policy)
        xstart = cls.value2xvalue(start, clusivities[0])
        xend = cls.value2xvalue(end, clusivities[1])

        return xstart, xend
