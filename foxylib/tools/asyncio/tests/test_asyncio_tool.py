import asyncio
import sys
from unittest import TestCase

from future.utils import lmap

from foxylib.tools.asyncio.asyncio_tool import AsyncioTool
from foxylib.tools.collections.collections_tool import smap


class TestNative(TestCase):

    @classmethod
    @asyncio.coroutine
    def countdown_coroutine(cls, number, n):
        while n > 0:
            print("T-minus", n, "({})".format(number))
            yield from asyncio.sleep(1)
            n -= 1


    def test_01(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())

            tasks = [asyncio.ensure_future(cls.countdown_coroutine("A", 2), loop=loop),
                     asyncio.ensure_future(cls.countdown_coroutine("B", 3), loop=loop),
                     ]
            loop.run_until_complete(asyncio.wait(tasks))

            print("hello world", file=sys.stderr)

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        # loop_system.close()  # do not close the loop if using asyncio.get_event_loop()

        loop_new = asyncio.new_event_loop()  # not working. closed when test closes
        subtest(loop_new)
        loop_new.close()  # can close because loop is from asyncio.new_event_loop()

    @classmethod
    async def countdown_async(cls, label, n):
        while n > 0:
            print("T-minus", n, "({})".format(label), file=sys.stderr)
            await asyncio.sleep(1)
            n -= 1
        return label


    def test_02(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())


            futures = [cls.countdown_async("A", 3),
                       cls.countdown_async("B", 2),
                       ]
            tasks_done, tasks_pending = loop.run_until_complete(asyncio.wait(futures))
            print((tasks_done,tasks_pending), file=sys.stderr)
            self.assertEqual(smap(lambda task:task.result(), tasks_done), {"A","B"}) # order not guaranteed

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        # loop_system.close()  # do not close the loop if using asyncio.get_event_loop()

        loop_new = asyncio.new_event_loop()  # not working. closed when test closes
        subtest(loop_new)
        loop_new.close()  # can close because loop is from asyncio.new_event_loop()


    def test_03(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())

            tasks = [asyncio.ensure_future(cls.countdown_async("A", 2), loop=loop),
                     asyncio.ensure_future(cls.countdown_async("B", 3), loop=loop),
                     ]
            rv = loop.run_until_complete(asyncio.gather(*tasks))

            ref = ["A","B"]
            self.assertEqual(rv, ref)
            self.assertEqual(lmap(lambda task: task.result(), tasks), ref)

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        # loop_system.close()  # do not close the loop if using asyncio.get_event_loop()

        loop_new = asyncio.new_event_loop()  # not working. closed when test closes
        subtest(loop_new)
        loop_new.close()  # can close because loop is from asyncio.new_event_loop()


    def test_04(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())

            tasks = [cls.countdown_async("A", 2),
                     cls.countdown_async("B", 3),
                     ]
            rv = loop.run_until_complete(asyncio.gather(*tasks))

            self.assertEqual(rv, ["A","B"])
            # print(lmap(lambda coroutine:  coroutine.result(), tasks), file=sys.stderr) # this is an error

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        # loop_system.close()  # do not close the loop if using asyncio.get_event_loop()

        loop_new = asyncio.new_event_loop()  # not working. closed when test closes
        with self.assertRaises(Exception): # can't have different loop
            subtest(loop_new)
        loop_new.close()  # can close because loop is from asyncio.new_event_loop()

class TestAsyncTool(TestCase):

    def test_01(self):
        coro_list = [TestNative.countdown_async("A", 2),
                     TestNative.countdown_async("B", 3),
                     ]
        hyp = AsyncioTool.awaitable_list2result_list(coro_list)
        ref = ["A","B"]

        self.assertEqual(hyp, ref)


    def test_02(self):
        coro_list = [TestNative.countdown_async("A", 2),
                     TestNative.countdown_async("B", 3),
                     ]
        loop = asyncio.new_event_loop()
        hyp = AsyncioTool.awaitable_list2result_list(coro_list, loop=loop)
        loop.close()
        ref = ["A","B"]

        self.assertEqual(hyp, ref)

