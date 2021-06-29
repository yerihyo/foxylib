import logging
from dataclasses import dataclass, asdict
from decimal import Decimal
from pprint import pformat
from typing import Union, Optional, TypeVar, Literal, Tuple, List

from foxylib.tools.collections.iter_tool import iter2singleton
from future.utils import lmap, lfilter
from nose.tools import assert_equal, assert_false, assert_not_equal, \
    assert_is_not_none, assert_true, assert_less_equal

from foxylib.tools.collections.collections_tool import AbsoluteOrder, DictTool, \
    merge_dicts, vwrite_skip_if_identical
from foxylib.tools.collections.dicttree.dictschema_tool import \
    DictschemaTool
from foxylib.tools.compare.minimax_tool import MinimaxTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import is_none

T = TypeVar("T")

class IntervalTool:
    class Clusivity:
        IN = CLOSED = True
        EX = OPEN = False

        @classmethod
        def typechecked(cls, inex):
            if not isinstance(inex, bool):
                raise ValueError({'inex':inex})
            return inex

    @classmethod
    def type(cls):
        return Tuple[cls.Point, cls.Point]

    @classmethod
    def fit2interval(cls, value, interval, tick=None):
        cmp = cls.value2cmp(interval, value)

        if cmp < 0:
            spoint = cls.interval2spoint(interval)
            start = cls.Point.point2value(spoint)
            if cls.Point.point2is_closed(spoint):
                return start

            if tick:
                return start + tick

            raise ValueError("Cannot compute start")

        if cmp > 1:
            epoint = cls.interval2epoint(interval)
            end = cls.Point.point2value(epoint)
            if cls.Point.point2is_closed(epoint):
                return end

            if tick:
                return end - tick

            raise ValueError("Cannot compute end")

        return value

    @dataclass(frozen=True)
    class Point:
        value: Optional[T]
        position: "IntervalTool.Point.Position.type()"
        inex: bool

        class Value:
            INF = None

        class Position:
            START = 'start'
            END = 'end'

            @classmethod
            def type(cls):
                return Literal["start", "end"]

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
        def cmp(cls, point1, point2):
            return cls.compare(point1, point2)

        @classmethod
        def gt(cls, point1, point2):
            return cls.compare(point1, point2) > 0

        @classmethod
        def gte(cls, point1, point2):
            return cls.compare(point1, point2) >= 0

        @classmethod
        def lt(cls, point1, point2):
            return cls.compare(point1, point2) < 0

        @classmethod
        def lte(cls, point1, point2):
            return cls.compare(point1, point2) <= 0

        @classmethod
        def eq(cls, point1, point2):
            return cls.equals(point1, point2)

        @classmethod
        def ne(cls, point1, point2):
            return not cls.eq(point1, point2)

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
        def spoints2max(cls, spoints_in: List[dict]):
            for spoint_in in spoints_in:
                assert_equal(spoint_in.get(cls.Field.POSITION), cls.Position.START)

            v = max(lmap(cls.point2value, spoints_in), key=AbsoluteOrder.null2min)

            # values = lmap(AbsoluteOrder.null2min, map(cls.point2value, spoints_in))
            # indexes_max = MinimaxTool.indexes_max(values)
            spoints_max = filter(lambda p: cls.point2value(p) == v, spoints_in)
            # v = iter2singleton(map(lambda i: values[i], indexes_max))
            inex = all(map(cls.point2inex, spoints_max))

            spoint_out = {cls.Field.VALUE: v,
                          cls.Field.INEX: inex,
                          }
            return spoint_out

        @classmethod
        def epoints2min(cls, epoints_in:List[dict]):
            logger = FoxylibLogger.func_level2logger(cls.epoints2min, logging.DEBUG)

            for epoint in epoints_in:
                assert_equal(epoint[cls.Field.POSITION], cls.Position.END)

            # logger.debug({'epoints':epoints})

            v = min(lmap(cls.point2value, epoints_in), key=AbsoluteOrder.null2max)
            epoints_min = filter(lambda p: cls.point2value(p) == v, epoints_in)
            inex = all(map(cls.point2inex, epoints_min))
            epoint_out = {cls.Field.VALUE: v,
                          cls.Field.INEX: inex,
                          }
            return epoint_out

        @classmethod
        def value2point(cls, v, inex_in:bool, position,) -> "IntervalTool.Point":
            # IntervalTool.Clusivity.typechecked(inex_in)

            inex_out = IntervalTool.Clusivity.EX if v is None else inex_in

            point = cls(value=v,
                        inex=inex_out,
                        position=position,
            )
            return point

    class Policy:
        INEX = "inex"
        ININ = "inin"
        EXEX = "exex"
        EXIN = "exin"

        @classmethod
        def policy2inex_pair(cls, policy):
            return (policy in {cls.ININ, cls.INEX},
                    policy in {cls.ININ, cls.EXIN}
                    )

        @classmethod
        def policy2inex_start(cls, policy):
            return cls.policy2inex_pair(policy)[0]

        @classmethod
        def policy2inex_end(cls, policy):
            return cls.policy2inex_pair(policy)[1]


    # class Section:
    #     BEFORE = "before"
    #     IN = "in"
    #     AFTER = "after"
    #
    #     @classmethod
    #     def type(cls):
    #         return Literal["before", "in", "after"]

    @classmethod
    def value2cmp(cls, interval, value) -> Optional[Literal[-1, 0, 1]]:
        if not cls.interval2bool(interval):
            return None

        spoint, epoint = interval
        start, end = lmap(cls.Point.point2value, interval)

        if value < start:
            return -1
        if start < value < end:
            return 0
        if value > end:
            return 1

        if value == start:
            if cls.Point.point2is_closed(spoint):
                return 0
            else:
                return -1

        if value == end:
            if cls.Point.point2is_closed(epoint):
                return 0
            else:
                return 1

        raise NotImplementedError({'interval':interval, 'value':value})


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
        if not interval:
            return None

        return cls.interval2end(interval) - cls.interval2start(interval)

    @classmethod
    def interval2spoint(cls, interval):
        return merge_dicts([interval[0], {'position':IntervalTool.Point.Position.START}],
                    vwrite=DictTool.VWrite.skip_if_identical)

    @classmethod
    def interval2epoint(cls, interval):
        return merge_dicts([interval[1], {'position': IntervalTool.Point.Position.END}],
                           vwrite=DictTool.VWrite.skip_if_identical)

    @classmethod
    def intersect(cls, intervals):
        logger = FoxylibLogger.func_level2logger(cls.intersect, logging.DEBUG)

        if any(map(is_none, intervals)):
            return None
            # return False

        # logger.debug(pformat({
        #     'intervals':intervals,
        # }))

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
        if interval is None:
            return False

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
    def filter_covered(cls, iter_in, interval):
        for x in iter_in:
            cmp = cls.value2cmp(interval, x)
            if cmp == 0:
                yield x

    # @classmethod
    # def iter2span_covered(cls, iter_in, interval):
    #     for i, x in enumerate(iter_in):
    #         cls.value2cmp(interval, v)

    @classmethod
    def interval2span(cls, interval):
        if interval is None:
            return None

        return lmap(cls.Point.point2value, interval)

    @classmethod
    def start2interval_gt(cls, start, policy):
        return cls.span2interval((start, None), policy)

    @classmethod
    def end2interval_lt(cls, end, policy):
        return cls.span2interval((None, end), policy)

    @classmethod
    def span2interval(cls, span, policy) -> Optional[Tuple[dict,dict]]:
        logger = FoxylibLogger.func_level2logger(
            cls.span2interval, logging.DEBUG)

        if not span:
            return None

        start, end = span

        inex_pair = cls.Policy.policy2inex_pair(policy)

        s_inex = inex_pair[0] if start is not None else False
        spoint = cls.Point(value=start, position='start', inex=s_inex)
            # .value2point(start, s_inex)

        e_inex = inex_pair[1] if end is not None else False
        epoint = cls.Point(value=end, position='end', inex=e_inex)

        return asdict(spoint), asdict(epoint)

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


