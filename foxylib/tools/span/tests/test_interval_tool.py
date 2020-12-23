import logging
from unittest import TestCase

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
