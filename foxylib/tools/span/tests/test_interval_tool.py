import logging
from datetime import datetime
from pprint import pprint
from unittest import TestCase

import pytz

from foxylib.tools.span.interval_tool import IntervalTool

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestIntervalTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        spoint1 = {'value': 3, 'inex': True, 'position': 'start'}
        epoint1 = {'value': 3, 'inex': True, 'position': 'end'}

        spoint2 = {'value': 3, 'inex': False, 'position': 'start'}
        epoint2 = {'value': 3, 'inex': False, 'position': 'end'}

        spoint3 = {'value': 5, 'inex': True, 'position': 'start'}
        epoint3 = {'value': 5, 'inex': True, 'position': 'end'}

        spoint4 = {'value': 5, 'inex': False, 'position': 'start'}
        epoint4 = {'value': 5, 'inex': False, 'position': 'end'}

        self.assertEqual(IntervalTool.Point.cmp(spoint1, spoint1,), 0)
        self.assertEqual(IntervalTool.Point.cmp(spoint1, epoint1,), 0)
        self.assertEqual(IntervalTool.Point.cmp(epoint1, epoint1), 0)
        self.assertTrue(IntervalTool.Point.eq(spoint1, spoint1,))
        self.assertTrue(IntervalTool.Point.eq(spoint1, epoint1,))
        self.assertTrue(IntervalTool.Point.eq(epoint1, epoint1,))
        self.assertFalse(IntervalTool.Point.ne(spoint1, spoint1,))
        self.assertFalse(IntervalTool.Point.ne(spoint1, epoint1,))
        self.assertFalse(IntervalTool.Point.ne(epoint1, epoint1,))

        self.assertLess(IntervalTool.Point.cmp(spoint1, spoint2, ), 0)
        self.assertGreater(IntervalTool.Point.cmp(spoint1, epoint2, ), 0)
        self.assertLess(IntervalTool.Point.cmp(epoint1, spoint2, ), 0)
        self.assertGreater(IntervalTool.Point.cmp(epoint1, epoint2, ), 0)

        self.assertTrue(IntervalTool.Point.lt(spoint1, spoint2, ))
        self.assertTrue(IntervalTool.Point.lte(spoint1, spoint2, ))
        self.assertFalse(IntervalTool.Point.gt(spoint1, spoint2, ))
        self.assertFalse(IntervalTool.Point.gte(spoint1, spoint2, ))
        self.assertFalse(IntervalTool.Point.eq(spoint1, spoint2, ))
        self.assertTrue(IntervalTool.Point.ne(spoint1, spoint2, ))

        self.assertLess(IntervalTool.Point.cmp(spoint1, spoint4, ),0)
        self.assertLess(IntervalTool.Point.cmp(spoint1, epoint4, ),0)
        self.assertLess(IntervalTool.Point.cmp(epoint1, spoint4, ),0)
        self.assertLess(IntervalTool.Point.cmp(epoint1, epoint4, ),0)

        self.assertLess(IntervalTool.Point.cmp(spoint2, spoint3, ),0)
        self.assertLess(IntervalTool.Point.cmp(spoint2, epoint3, ),0)
        self.assertLess(IntervalTool.Point.cmp(epoint2, spoint3, ),0)
        self.assertLess(IntervalTool.Point.cmp(epoint2, epoint3, ),0)

    def test_02(self):
        intervals = [({'inex': False, 'value': None},
                      {'inex': False, 'value': datetime(2020, 1, 1, 0, 31, tzinfo=pytz.utc)}),
                     ({'inex': False, 'value': None},
                      {'inex': False, 'value': None}),
                     ({'inex': False, 'value': None},
                      {'inex': True,'value': datetime(2021, 3, 30, 1, 43, 28, 725000, tzinfo=pytz.utc)}
                      )]
        hyp = IntervalTool.intersect(intervals)
        ref = ({'inex': False, 'value': None},
               {'inex': False, 'value': datetime(2020, 1, 1, 0, 31, tzinfo=pytz.utc)})

        # pprint({'hyp':hyp, 'ref':ref})
        self.assertEqual(hyp, ref)

    def test_03(self):
        intervals = [({'inex': False, 'position': 'start', 'value': None},
                      {'inex': False, 'position': 'end', 'value': None},),
                     ({'inex': False, 'position': 'start', 'value': None},
                      {'inex': False,
                       'position': 'end',
                       'value': datetime(2020, 1, 1, 0, 0, tzinfo=pytz.utc)},),
                     ({'inex': True,
                       'position': 'start',
                       'value': datetime(2020, 1, 1, 0, 0, tzinfo=pytz.utc)},
                       {'inex': False,
                        'position': 'end',
                        'value': datetime(2020, 1, 1, 0, 31, tzinfo=pytz.utc)}),
                     ]
        hyp = IntervalTool.intersect(intervals)
        ref = None

        self.assertEqual(hyp, ref)

    def test_4(self):
        hyp1 = list(IntervalTool.values2bucketindexes(
            [0, 0, 4, 8, 10, 12],
            [2, 3, 4, 9, 12],
            IntervalTool.Policy.INEX,
        ))
        ref1 = [0, 0, 3, 3, 4, 5]
        self.assertEqual(hyp1, ref1)

        hyp2 = list(IntervalTool.values2bucketindexes(
            [0, 0, 4, 8, 10, 12],
            [2, 3, 4, 9, 12],
            IntervalTool.Policy.EXIN,
        ))
        ref2 = [0, 0, 2, 3, 4, 4]
        self.assertEqual(hyp2, ref2)

    def test_5(self):
        dt_action = datetime(2021, 9, 17, 22, 38, 26, 898000, tzinfo=pytz.utc)
        dt_interval = (
            {'value': datetime(2021, 9, 17, 22, 38, 16, 898000, tzinfo=pytz.utc),'position': 'start', 'inex': False},
            {'value': datetime(2021, 9, 17, 22, 38, 26, 898000, tzinfo=pytz.utc), 'position': 'end', 'inex': True},
        )
        self.assertTrue(IntervalTool.is_in(dt_action, dt_interval))
