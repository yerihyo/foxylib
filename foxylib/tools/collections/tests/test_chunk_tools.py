import logging
from unittest import TestCase

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.collections.chunk_tool import ChunkTool


class TestChunkTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):

        x_iter = range(20)
        f_batch = lambda l:[min(l)]*len(l)
        f_cond = lambda x:x%2==0
        y_iter = ChunkTool.iter_batch_cond2processed(x_iter, f_batch, f_cond, (2,10))
        hyp = list(y_iter)
        ref = [0, 1, 0, 3, 4, 5, 4, 7, 8, 9, 8, 11, 12, 13, 12, 15, 16, 17, 16, 19]

        # pprint(hyp)

        self.assertEqual(hyp, ref)

    def test_02(self):
        x_iter = range(20)
        f_batch = lambda l:[min(l)]*len(l)
        f_cond = lambda x:x%2==0
        y_iter = ChunkTool.iter_batch_cond2processed(x_iter, f_batch, f_cond, (3,4))
        hyp = list(y_iter)
        ref = [0, 1, 0, 3, 4, 5, 4, 7, 8, 9, 8, 11, 12, 13, 12, 15, 16, 17, 16, 19]

        # pprint(hyp)

        self.assertEqual(hyp, ref)

    def test_03(self):
        self.assertEqual(
            list(ChunkTool.grouper(4, range(6))),
            [(0, 1, 2, 3), (4, 5)])
        self.assertEqual(
            list(ChunkTool.grouper(4, range(9))),
            [(0, 1, 2, 3), (4, 5, 6, 7), (8,)])
        self.assertEqual(
            list(ChunkTool.grouper(4, range(3))),
            [(0, 1, 2,)])

    def test_04(self):
        self.assertEqual(
            list(ChunkTool.chunk_count2endindexes(6, 4)), [1, 3, 4, 6])
        self.assertEqual(
            list(ChunkTool.chunk_count2endindexes(9, 4)), [2, 4, 6, 9])
        self.assertEqual(
            list(ChunkTool.chunk_count2endindexes(3, 4)), [0, 1, 2, 3])

    def test_05(self):
        self.assertEqual(
            list(ChunkTool.chunk_count2chunk_sizes(6, 4)), [1, 2, 1, 2])
        self.assertEqual(
            list(ChunkTool.chunk_count2chunk_sizes(9, 4)), [2, 2, 2, 3])
        self.assertEqual(
            list(ChunkTool.chunk_count2chunk_sizes(3, 4)), [0, 1, 1, 1])
