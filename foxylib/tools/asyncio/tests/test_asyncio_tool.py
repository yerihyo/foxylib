import asyncio
import logging
import random
import sys
from collections import deque
from functools import partial
from unittest import TestCase

from aiostream import stream
from future.utils import lmap

from foxylib.tools.asyncio.asyncio_tool import AioTool
from foxylib.tools.collections.collections_tool import smap
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class P2C:
    @classmethod
    async def rnd_sleep(cls, t):
        # sleep for T seconds on average
        await asyncio.sleep(t * random.random() * 2)

    @classmethod
    async def producer(cls, queue, produced):
        while True:
            token = random.random()
            print(f'produced {token}')
            if token < .05:
                break

            await queue.put(token)
            produced.append(token)

            await cls.rnd_sleep(.1)

    @classmethod
    async def consumer(cls, queue, consumed):
        while True:
            token = await queue.get()
            consumed.append(token)

            await cls.rnd_sleep(.3)
            queue.task_done()
            print(f'consumed {token}')


class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

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

            futures = [asyncio.ensure_future(cls.countdown_coroutine("A", 2), loop=loop),
                       asyncio.ensure_future(cls.countdown_coroutine("B", 3), loop=loop),
                       ]
            loop.run_until_complete(asyncio.wait(futures))

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

            coros = [cls.countdown_async("A", 3),
                     cls.countdown_async("B", 2),
                     ]
            # tasks_done, tasks_pending = loop.run_until_complete(asyncio.wait(coros))
            tasks_done, tasks_pending = loop.run_until_complete(asyncio.wait(coros, loop=loop))
            print((tasks_done, tasks_pending), file=sys.stderr)
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

            tasks = [cls.countdown_async("A", 2),  # not using loop parameter
                     cls.countdown_async("B", 3),
                     ]
            rv = loop.run_until_complete(asyncio.gather(*tasks))

            self.assertEqual(rv, ["A","B"])
            # print(lmap(lambda coroutine:  coroutine.result(), tasks), file=sys.stderr) # this is an error

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        # loop_system.close()  # do not close the loop if using asyncio.get_event_loop()

        loop_new = asyncio.new_event_loop()  # not working. closed when test closes
        with self.assertRaises(Exception):  # can't have different loop
            subtest(loop_new)
        loop_new.close()  # can close because loop is from asyncio.new_event_loop()

    def test_05(self):
        cls = self.__class__

        def subtest():
            tasks = [cls.countdown_async("A", 2),  # not using loop parameter
                     cls.countdown_async("B", 3),
                     ]
            rv = asyncio.run(asyncio.gather(*tasks))  # asyncio.run always creates new loop

            self.assertEqual(rv, ["A", "B"])

        # https://bugs.python.org/issue36222#msg337376
        # asyncio.gather() creates a future linked to loop (current loop if no loop)
        # asyncio.run() tries to create its own loop
        # these two collide
        with self.assertRaises(Exception):
            subtest()

    def test_06(self):
        async def iter1():
            for _ in range(5):
                await asyncio.sleep(0.1)
                yield 1

        async def iter2():
            for _ in range(5):
                await asyncio.sleep(0.2)
                yield 2

        aiter_merged = AioTool.aiters2merged([iter1(), iter2()])
        rv = asyncio.run(AioTool.aiter2list(aiter_merged))
        self.assertEqual(sorted(rv), [1, 1, 1, 1, 1, 2, 2, 2, 2, 2])

    def test_07(self):
        # https://asyncio.readthedocs.io/en/latest/producer_consumer.html

        async def produce(queue, n):
            print("start produce()")

            for x in range(n):
                # produce an item
                print('producing {}/{}'.format(x, n))
                # simulate i/o operation using sleep
                await asyncio.sleep(random.random())
                item = str(x)
                # put the item in the queue
                await queue.put(item)

        async def consume(queue):
            print("start consume()")

            while True:
                # wait for an item from the producer
                item = await queue.get()

                # process the item
                print('consuming {}...'.format(item))
                # simulate i/o operation using sleep
                await asyncio.sleep(random.random())

                # Notify the queue that the item has been processed
                queue.task_done()

        async def run(n):
            queue = asyncio.Queue()
            # schedule the consumer
            consumer = asyncio.ensure_future(consume(queue))
            # run the producer and wait for completion
            await produce(queue, n)
            # wait until the consumer has processed all items
            print("start join()")
            await queue.join()
            # the consumer is still awaiting for an item, cancel it
            consumer.cancel()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(10))
        loop.close()

    def test_08(self):
        produced = deque()
        consumed = deque()

        async def main():
            queue = asyncio.Queue()


            # fire up the both producers and consumers
            producers = [asyncio.create_task(P2C.producer(queue, produced))
                         for _ in range(3)]
            consumers = [asyncio.create_task(P2C.consumer(queue, consumed))
                         for _ in range(10)]

            # with both producers and consumers running, wait for
            # the producers to finish
            await asyncio.gather(*producers)
            print('---- done producing')

            # wait for the remaining tasks to be processed
            await queue.join()

            # cancel the consumers, which are now idle
            for c in consumers:
                c.cancel()

        asyncio.run(main())
        self.assertEqual(sorted(produced), sorted(consumed))



class TestAsyncTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        coro_list = [TestNative.countdown_async("A", 2),
                     TestNative.countdown_async("B", 3),
                     ]
        hyp = AioTool.awaitables2result_list(coro_list)
        ref = ["A","B"]

        self.assertEqual(hyp, ref)


    def test_02(self):
        coro_list = [TestNative.countdown_async("A", 2),
                     TestNative.countdown_async("B", 3),
                     ]
        loop = asyncio.new_event_loop()
        hyp = AioTool.awaitables2result_list(coro_list, loop=loop)
        loop.close()
        ref = ["A","B"]

        self.assertEqual(hyp, ref)

    def test_03(self):
        produced = []
        consumed = []

        producer_list = [partial(P2C.producer, produced=produced) for x in range(3)]
        consumer_list = [partial(P2C.consumer, consumed=consumed) for x in range(10)]
        asyncio.run(AioTool.produce_consume(producer_list, consumer_list))

        self.assertEqual(sorted(produced), sorted(consumed))

