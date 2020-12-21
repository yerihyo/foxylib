import logging
from decimal import Decimal
from pprint import pformat
from typing import Union, Optional

from foxylib.tools.collections.iter_tool import iter2singleton
from future.utils import lmap, lfilter
from nose.tools import assert_equal, assert_false, assert_not_equal, \
    assert_is_not_none, assert_true

from foxylib.tools.collections.collections_tool import AbsoluteOrder, DictTool, \
    merge_dicts, vwrite_skip_if_identical
from foxylib.tools.collections.dicttree.dictschema_tool import \
    DictschemaTool
from foxylib.tools.compare.minimax_tool import MinimaxTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class IntervalTool:
    class Clusivity:
        IN = CLOSED = True
        EX = OPEN = False

        @classmethod
        def typechecked(cls, inex):
            if not isinstance(inex, bool):
                raise ValueError({'inex':inex})
            return inex

    class Point:
        class Value:
            INF = None

        class Position:
            START = 'start'
            END = 'end'

            @classmethod
            def values(cls):
                return {cls.START, cls.END}

        class Field:
            VALUE = "value"
            CLUSIVITY = INEX = "inex"
            POSITION = 'position'

        @classmethod
        def schema(cls):
            return {
                'inex': bool,
                'value': Union[int, Decimal, float, None],  # None for inf
                'position': Optional[str]
            }

        @classmethod
        def typechecked(cls, point):
            DictschemaTool.tree2typechecked(point, cls.schema())

            position = cls.point2position(point)

            if position not in {None, *cls.Position.values()}:
                raise ValueError({'point': point})
            return point

        @classmethod
        def equals(cls, point1, point2):
            value1, inex1, position1 = cls.point2value_inex_position(point1)
            value2, inex2, position2 = cls.point2value_inex_position(point2)

            if (value1, inex1, position1) == (value2, inex2, position2):
                return True

            if (value1 is None) or (value2 is None):  # inf and not equal
                return False

            assert_is_not_none(value1)
            assert_is_not_none(value2)

            if (value1, inex1) != (value2, inex2):
                return False

            assert_equal((value1, inex1), (value2, inex2))
            assert_not_equal(position1, position2)

            if inex1 is True:
                assert_true(inex2)
                return True

            if inex1 is False:
                assert_false(inex2)
                return False

            raise NotImplementedError(
                {'point1': point1, 'point2': point2})

        @classmethod
        def is_inf(cls, point):
            value, inex, position = cls.point2value_inex_position(point)
            if value is not None:
                return False

            assert_false(inex)
            return True

        @classmethod
        def is_neg_inf(cls, point):
            if not cls.is_inf(point):
                return False

            return cls.point2position(point) == cls.Position.START

        @classmethod
        def is_pos_inf(cls, point):
            if not cls.is_inf(point):
                return False

            return cls.point2position(point) == cls.Position.END

        @classmethod
        def compare(cls, point1, point2):
            logger = FoxylibLogger.func_level2logger(
                cls.compare, logging.DEBUG)

            if cls.equals(point1, point2):
                return 0

            # inf
            if cls.is_inf(point1):
                if cls.is_pos_inf(point1):
                    return 1
                if cls.is_neg_inf(point1):
                    return -1

                raise NotImplementedError(
                    {'point1': point1, 'point2': point2})

            if cls.is_inf(point2):  # is inf
                return -1 * cls.compare(point2, point1)

            value1, inex1, position1 = cls.point2value_inex_position(point1)
            value2, inex2, position2 = cls.point2value_inex_position(point2)

            assert_is_not_none(value1)
            assert_is_not_none(value2)

            if value1 != value2:
                return 1 if value1 > value2 else -1

            assert_equal(value1, value2)
            assert_not_equal(inex1, inex2)  # if equal then .equals()

            if (position1 is None) or (position2 is None):
                raise NotImplementedError(pformat({
                    'point1': point1, 'point2': point2
                }))

            assert_is_not_none(position1)
            assert_is_not_none(position2)

            if position1 != position2:
                if position1 == cls.Position.START:
                    return 1
                if position1 == cls.Position.END:
                    return -1
                raise ValueError({'position1':position1})

            assert_equal(position1, position2)

            if position1 == cls.Position.START:
                if inex1:
                    assert_false(inex2)
                    return -1
                else:
                    assert_true(inex2)
                    return 1

            if position1 == cls.Position.END:
                if inex1:
                    assert_false(inex2)
                    return 1
                else:
                    assert_true(inex2)
                    return -1

            raise NotImplementedError(pformat({
                'point1': point1, 'point2': point2
            }))

        @classmethod
        def inf(cls):
            return cls.typechecked({'value': None, 'inex': False})

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
        def point2value_inex_position(cls, point):
            value = point[cls.Field.VALUE]
            inex = point[cls.Field.INEX]
            position = point.get(cls.Field.POSITION)
            return value, inex, position

        @classmethod
        def point2value_inex(cls, point):
            x = cls.point2value_inex_position(point)
            return x[:2]

        @classmethod
        def point2position(cls, point):
            x = cls.point2value_inex_position(point)
            return x[2]

        @classmethod
        def spoints2max(cls, spoints_in):
            values = lmap(AbsoluteOrder.null2min, map(cls.point2value, spoints_in))
            indexes_max = MinimaxTool.indexes_max(values)
            spoints_max = lmap(lambda i: spoints_in[i], indexes_max)
            v = iter2singleton(map(lambda i: values[i], indexes_max))
            inex = all(map(cls.point2inex, spoints_max))

            spoint_out = {cls.Field.VALUE: v,
                          cls.Field.INEX: inex,
                          }
            return spoint_out

        @classmethod
        def epoints2min(cls, epoints):
            logger = FoxylibLogger.func_level2logger(
                cls.epoints2min, logging.DEBUG)

            # logger.debug({'epoints':epoints})

            v = min(lmap(cls.point2value, epoints), key=AbsoluteOrder.null2max)
            epoints_min = filter(lambda p: cls.point2value(p) == v, epoints)
            inex = all(map(cls.point2inex, epoints_min))
            epoint_out = {cls.Field.VALUE: v,
                          cls.Field.INEX: inex,
                          }
            return epoint_out

        @classmethod
        def value2point(cls, v, inex_in, position=None,):
            IntervalTool.Clusivity.typechecked(inex_in)

            inex_out = IntervalTool.Clusivity.EX if v is None else inex_in

            point = {cls.Field.VALUE: v,
                     cls.Field.CLUSIVITY: inex_out,
                     }

            if not position:
                point_out = point
            else:
                point_out = merge_dicts(
                    [point, {cls.Field.POSITION: position}],
                    vwrite=DictTool.VWrite.no_duplicate_key)

            return point_out

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
    def bool(cls, interval):
        if not interval:
            return False

        return True

    @classmethod
    def typechecked(cls, interval):
        if len(interval) != 2:
            raise ValueError({'interval': interval})

        for point in interval:
            cls.Point.typechecked(point)

        spoint, epoint = interval

        if cls.Point.point2position(spoint) not in {None, 'start'}:
            raise ValueError({'spoint': spoint})

        if cls.Point.point2position(spoint) not in {None, 'end'}:
            raise ValueError({'epoint': epoint})

        return interval

    @classmethod
    def norm(cls, interval):
        cls.typechecked(interval)
        return lmap(lambda p: p.pop([cls.Point.Field.POSITION], interval))

    @classmethod
    def inf(cls):
        interval = ({'value': None, 'inex': False,},
                    {'value': None, 'inex': False,},
                    )
        return cls.typechecked(interval)

    @classmethod
    def value2interval_inclusive(cls, value):
        span = [value, value]
        interval = cls.span2interval(span, cls.Policy.ININ)
        return interval

    @classmethod
    def value2is_inf(cls, value):
        return value is cls.Point.Value.INF

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
    def interval2spoint(cls, interval):
        return interval[0]

    @classmethod
    def interval2epoint(cls, interval):
        return interval[1]

    @classmethod
    def intersect(cls, intervals):
        logger = FoxylibLogger.func_level2logger(cls.intersect, logging.DEBUG)

        spoints = lmap(cls.interval2spoint, intervals)
        epoints = lmap(cls.interval2epoint, intervals)

        # logger.debug(pformat({
        #     'intervals': intervals,
        #     'spoints': spoints,
        #     'epoints': epoints,
        # }))
        # raise Exception()

        spoint = cls.Point.spoints2max(spoints)
        epoint = cls.Point.epoints2min(epoints)
        interval_out = spoint, epoint

        # logger.debug(pformat({
        #     'intervals': intervals,
        #     'spoints': spoints,
        #     'epoints': epoints,
        #     'spoint': spoint,
        #     'epoint': epoint,
        # }))
        # raise Exception({'interval_out':interval_out})

        if not cls.interval2has_span(interval_out):
            return None

        return interval_out

    @classmethod
    def cap(cls, intervals):
        return cls.intersect(intervals)

    @classmethod
    def overlaps(cls, interval1, interval2):
        logger = FoxylibLogger.func_level2logger(cls.overlaps, logging.DEBUG)

        interval = cls.intersect([interval1, interval2])
        # logger.debug({'interval': interval, 'interval1': interval1,
        #               'interval2': interval2})

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
        logger = FoxylibLogger.func_level2logger(
            cls.span2interval, logging.DEBUG)

        if not span:
            return None

        start, end = span

        inex_pair = cls.Policy.policy2clusivities(policy)

        s_inex = inex_pair[0] if start is not None else False
        spoint = cls.Point.value2point(start, s_inex)

        e_inex = inex_pair[1] if end is not None else False
        epoint = cls.Point.value2point(end, e_inex)

        logger.debug({
            'span':span,
            'spoint':spoint,
            'epoint':epoint,
        })

        return spoint, epoint

    @classmethod
    def spoint2interval_inf(cls, spoint):
        cls.Point.typechecked(spoint)
        epoint = {'value':None, 'inex':False}

        interval = (spoint, epoint)
        return cls.typechecked(interval)

    @classmethod
    def epoint2interval_inf(cls, epoint):
        cls.Point.typechecked(epoint)
        spoint = {'value': None, 'inex': False}

        interval = (spoint, epoint)
        return cls.typechecked(interval)


