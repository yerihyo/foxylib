from operator import itemgetter as ig

from foxylib.tools.collections.collections_tool import AbsoluteOrder
from future.utils import lmap
from nose.tools import assert_equal, assert_false


class IntervalTool:
    class Constant:
        INF = None

    class Clusivity:
        IN = CLOSED = True
        EX = OPEN = False

    class Point:
        class Field:
            VALUE = "value"
            CLUSIVITY = INEX = "inex"

        @classmethod
        def point2value(cls, point):
            return point[cls.Field.VALUE]

        @classmethod
        def point2inex(cls, point):
            return point[cls.Field.INEX]

        @classmethod
        def point2is_inclusive(cls, point):
            return cls.point2inex(point)

        @classmethod
        def point2is_closed(cls, point):
            return cls.point2inex(point)

        @classmethod
        def point2is_open(cls, point):
            return not cls.point2is_closed(point)

        @classmethod
        def point2value_inex(cls, point):
            value = point[cls.Field.VALUE]
            inex = point[cls.Field.INEX]
            return value, inex

        @classmethod
        def spoints2max(cls, spoints):
            v = max(lmap(cls.point2value, spoints), key=AbsoluteOrder.null2min)
            spoints_max = filter(lambda p: cls.point2value(p) == v, spoints)
            inex = all(map(cls.point2inex, spoints_max))

            spoint_out = {cls.Field.VALUE: v,
                          cls.Field.INEX: inex,
                          }
            return spoint_out

        @classmethod
        def epoints2min(cls, epoints):
            v = min(lmap(cls.point2value, epoints), key=AbsoluteOrder.null2max)
            epoints_min = filter(lambda p: cls.point2value(p) == v, epoints)
            inex = all(map(cls.point2inex, epoints_min))
            epoint_out = {cls.Field.VALUE: v,
                          cls.Field.INEX: inex,
                          }
            return epoint_out

        @classmethod
        def value2point(cls, v, inex_in):
            inex_out = IntervalTool.Clusivity.EX if v is None else inex_in

            point = {cls.Field.VALUE: v,
                     cls.Field.CLUSIVITY: inex_out
                     }
            return point

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
    def interval2bool(cls, interval):
        return cls.interval2has_span(interval)

    @classmethod
    def interval2has_span(cls, interval):
        if not interval:
            return False

        (s, s_inex), (e, e_inex) = lmap(cls.Point.point2value_inex, interval)

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

    # @classmethod
    # def point2is_inclusive(cls, point):
    #     return cls.Point.point2inex(point)

    # @classmethod
    # def interval2clusivities(cls, interval):
    #     return lmap(cls.Point.point2inex, interval)

    @classmethod
    def interval2len(cls, interval):
        return cls.interval2end(interval) - cls.interval2start(interval)

    @classmethod
    def intersect(cls, interval1, interval2):
        spoint1, epoint1 = interval1
        spoint2, epoint2 = interval2

        spoint = cls.Point.spoints2max([spoint1, spoint2])
        epoint = cls.Point.epoints2min([epoint1, epoint2])
        interval_out = spoint, epoint

        if not cls.interval2has_span(interval_out):
            return None

        return interval_out

    @classmethod
    def cap(cls, interval1, interval2):
        return cls.intersect(interval1, interval2)

    @classmethod
    def overlaps(cls, interval1, interval2):
        interval = cls.intersect(interval1, interval2)
        return interval is not None

    @classmethod
    def spoint2has_started(cls, spoint, value_pivot):
        s, s_index = cls.Point.point2value_inex(spoint)
        if cls.value2is_inf(s):
            return True

        if s < value_pivot:
            return True

        if s > value_pivot:
            return False

        assert_equal(s, value_pivot)
        return cls.Point.point2is_closed(spoint)

    @classmethod
    def epoint2has_ended(cls, epoint, value_pivot):
        e, e_index = cls.Point.point2value_inex(epoint)
        if cls.value2is_inf(e):
            return False

        if e < value_pivot:
            return True

        if e > value_pivot:
            return False

        assert_equal(e, value_pivot)
        return cls.Point.point2is_open(epoint)

    @classmethod
    def is_in(cls, v, interval):
        spoint, epoint = interval

        has_started = cls.spoint2has_started(spoint, v)
        if not has_started:
            return False

        has_ended = cls.epoint2has_ended(epoint, v)
        if has_ended:
            return False

        return True

    @classmethod
    def interval2key_sort(cls, interval):
        point_start, point_end = interval
        s, s_inex = IntervalTool.Point.point2value_inex(point_start)
        e, e_inex = IntervalTool.Point.point2value_inex(point_end)

        k = (s,
             -1 if s_inex else 0,
             e,
             1 if e_inex else 0,
             )

        return k

    @classmethod
    def interval2start(cls, interval):
        spoint, epoint = interval
        return cls.Point.point2value(spoint)

    @classmethod
    def interval2end(cls, interval):
        spoint, epoint = interval
        return cls.Point.point2value(epoint)


    @classmethod
    def interval2span(cls, interval):
        return lmap(cls.Point.point2value, interval)

    @classmethod
    def span2interval(cls, span, policy):
        start, end = span

        clusivities = cls.Policy.policy2clusivities(policy)
        spoint = cls.Point.value2point(start, clusivities[0])
        epoint = cls.Point.value2point(end, clusivities[1])

        return spoint, epoint
