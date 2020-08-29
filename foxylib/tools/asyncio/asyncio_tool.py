import asyncio
import logging
from asyncio import ensure_future, gather, get_event_loop
from datetime import datetime, timedelta

import pytz
from aiostream.stream import merge
from future.utils import lmap
from nose.tools import assert_false, assert_equal, assert_greater_equal, assert_true

from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.collections.iter_tool import iter2singleton, IterTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool


class AioTool:
    @classmethod
    def func2async(cls, f):
        async def af(*_, **__):
            return f(*_, **__)
        return af

    @classmethod
    async def iter2push(cls, q, iter):
        for x in iter:
            await q.put(x)

    @classmethod
    def awaitable2result(cls, awaitable, *_, **__):
        return l_singleton2obj(cls.awaitables2result_list([awaitable], *_, **__))


    @classmethod
    def awaitables2result_list(cls, awaitables, loop=None):
        if loop is None:
            loop = get_event_loop()

        assert_false(loop.is_closed())

        future_list = [ensure_future(x, loop=loop) for x in awaitables]
        result_list = loop.run_until_complete(gather(*future_list))
        return result_list

    @classmethod
    @VersionTool.inactive(reason="can't make it work. loop creation problem.")
    def awaitables2result_list_(cls, awaitables,):
        future_list = [asyncio.create_task(x, ) for x in awaitables]
        result_list = asyncio.run(gather(*future_list))
        return result_list

    @classmethod
    async def aiter2list(cls, aiter):
        return [x async for x in aiter]

    @classmethod
    async def aiters2merged(cls, aiters):
        async with merge(*aiters).stream() as streamer:
            async for item in streamer:
                yield item

    @classmethod
    async def aiter2chunks(cls, aiter, chunk_size):
        chunk = []
        async for item in aiter:
            chunk.append(item)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []

        if chunk:
            yield chunk

    @classmethod
    async def datetime2sleep(cls, dt):
        dt_now = datetime.now(pytz.utc)
        td = dt - dt_now
        secs_sleep = td / timedelta(seconds=1)
        await asyncio.sleep(secs_sleep)

    # class Decorator:
    #     @classmethod
    #     def async_generator2coroutine(cls, async_generator,):
    #         def wrapper()
    #             async def wrapped(*_, **__):
    #
    #         async def coroutine_wrapper(async_gen, args):
    #             try:
    #                 print(tuple([i async for i in async_gen(args)]))
    #             except ValueError:
    #                 print(tuple([(i, j) async for i, j in async_gen(args)]))


    @classmethod
    async def produce_consume(cls, queue, produce_coros, consume_coros):
        logger = FoxylibLogger.func_level2logger(cls.produce_consume, logging.DEBUG)

        producer_tasks = lmap(asyncio.create_task, produce_coros)
        consumer_tasks = lmap(asyncio.create_task, consume_coros)

        # with both producers and consumers running, wait for
        # the producers to finish
        await asyncio.gather(*producer_tasks)
        logger.debug('producers done')

        # wait for the remaining tasks to be processed
        await queue.join()
        logger.debug('consumers done')

        # cancel the consumers, which are now idle
        for c in consumer_tasks:
            c.cancel()
        logger.debug('cancelled')

    @classmethod
    async def coros_list2pipelined(cls, coros_list, queue_list):
        logger = FoxylibLogger.func_level2logger(cls.coros_list2pipelined, logging.DEBUG)
        n = len(coros_list)
        assert_greater_equal(n, 1)

        assert_equal(len(queue_list), n-1)
        tasks_list = [lmap(asyncio.create_task, coros) for coros in coros_list]

        await asyncio.gather(*tasks_list[0])
        logger.debug('{}/{} coros done'.format(1, n))

        for i in range(1,n):
            await queue_list[i - 1].join()
            logger.debug('{}/{} queue empty'.format(i, n-1))

            for c in tasks_list[i]:
                c.cancel()

            logger.debug('{}/{} coros done'.format(i+1, n))

    @classmethod
    async def queue2get_n(cls, queue, n):
        logger = FoxylibLogger.func_level2logger(cls.queue2get_n, logging.DEBUG)
        # logger.debug({"queue.qsize()":queue.qsize()})

        item_first = await queue.get()
        items = [item_first]
        # logger.debug({"items":items})

        try:
            # logger.debug({"n": n})
            for i in range(n-1):
                # logger.debug({"i": i})
                item = queue.get_nowait()
                items.append(item)
        except asyncio.QueueEmpty:
            pass

        # logger.debug({"return items": items})
        return items

    @classmethod
    def queue2tasks_done(cls, queue, count):
        for _ in range(count):
            queue.task_done()

    @classmethod
    async def funcs_list2pipelined(cls, funcs_list, queue_list=None):
        assert_true(funcs_list)
        n = len(funcs_list)

        batches_producer = funcs_list[0]
        batches_list_after = [[lambda l: f(iter2singleton(l)) for f in funcs]
                              for funcs in funcs_list[1:]
                              ]
        batches_list = [batches_producer, *batches_list_after]
        chunksize_list = [1 for _ in range(n-1)]

        return await cls.batches_list2pipelined(batches_list, chunksize_list, queue_list=queue_list)

    @classmethod
    async def batches_list2pipelined(cls, batches_list, chunksize_list, queue_list=None):
        logger = FoxylibLogger.func_level2logger(cls.batches_list2pipelined, logging.DEBUG)
        n = len(batches_list)

        if queue_list is None:
            queue_list = [asyncio.Queue() for _ in range(n-1)]

        assert_equal(len(queue_list), n - 1)
        assert_equal(len(chunksize_list), n - 1)

        async def batch2coro_head(batch):
            queue_out = queue_list[0]
            for item_out in batch():
                # logger.debug(f"head enqueue {item_out}")
                await queue_out.put(item_out)

        async def batch2coro_middle(batch, i):
            # logger.debug(f"middle init i:{i}")

            queue_in, queue_out = queue_list[i-1], queue_list[i]
            chunksize = chunksize_list[i-1]

            while True:
                # logger.debug({"queue_in.qsize()":queue_in.qsize(), "chunksize":chunksize})
                items_in = await cls.queue2get_n(queue_in, chunksize)
                # logger.debug(f"middle pipe items_in:{items_in}")

                items_out = batch(items_in)
                for item_out in items_out:
                    # logger.debug(f"middle pipe item_out:{item_out}")
                    await queue_out.put(item_out)

                cls.queue2tasks_done(queue_in, len(items_in))

        async def batch2coro_tail(batch):
            queue_in = queue_list[-1]
            chunksize = chunksize_list[-1]

            while True:
                items_in = await cls.queue2get_n(queue_in, chunksize)
                IterTool.consume(batch(items_in))
                cls.queue2tasks_done(queue_in, len(items_in))

        coros_head = lmap(batch2coro_head, batches_list[0])
        coros_tail = lmap(batch2coro_tail, batches_list[-1])
        coros_list_middle = [[batch2coro_middle(batch, i)
                              for batch in batches_list[i]]
                             for i in range(1, n - 1)]
        coros_list = [coros_head, *coros_list_middle, coros_tail]

        return await cls.coros_list2pipelined(coros_list, queue_list)

