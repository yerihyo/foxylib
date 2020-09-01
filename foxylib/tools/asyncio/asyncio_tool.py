import asyncio
import logging
from asyncio import ensure_future, gather, get_event_loop, Queue
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Optional, List

import pytz
from aiostream.stream import merge
from cachetools import LRUCache
from future.utils import lmap
from nose.tools import assert_false, assert_equal, assert_greater_equal, assert_true, assert_is_not_none

from foxylib.tools.cache.cache_manager import CacheManager
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
    def queue2iter(cls, q):
        yield from q._queue  # might be problematic in the future

    @classmethod
    def awaitable2result(cls, awaitable):
        return l_singleton2obj(cls.awaitables2result_list([awaitable]))


    @classmethod
    @VersionTool.inactive(reason="Using loop. loop should not be specified after python 3.8")
    def awaitables2result_list_(cls, awaitables, loop=None):
        if loop is None:
            loop = get_event_loop()

        assert_false(loop.is_closed())

        future_list = [ensure_future(x, loop=loop) for x in awaitables]
        result_list = loop.run_until_complete(gather(*future_list))
        return result_list

    @classmethod
    async def awaitables2coro_gathered(cls, awaitables):
        async def gathered():
            return await gather(*awaitables)
        return await gathered()

    @classmethod
    def awaitables2result_list(cls, awaitables,):
        return asyncio.run(cls.awaitables2coro_gathered(awaitables))

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
    def task_count2all_done(cls, count, queue,):
        for _ in range(count):
            queue.task_done()

    @classmethod
    def coros2all_done(cls, coros):
        return all(map(lambda c: c.done(), coros))

    @classmethod
    def iterable2f_agenerator(cls, iterable):
        """
        reference: https://stackoverflow.com/q/55812939
        :param iterable:
        :return:
        """
        class Aiter:
            def __init__(self):
                self.iter = iter(iterable)

            def __aiter__(self):  # no need async after python 3.7
                return self

            async def __anext__(self):
                try:
                    object = next(self.iter)
                except StopIteration:
                    raise StopAsyncIteration
                return object
        return Aiter

    @classmethod
    def iterable2aiter(cls, iterable):
        f_agenerator = cls.iterable2f_agenerator(iterable)
        return f_agenerator()


    @classmethod
    def f_generator2f_aiter(cls, f_generator):
        class AIterator:
            def __init__(self):
                self.iter = iter(f_generator())

            def __aiter__(self):  # no need async after python 3.7
                return self

            async def __anext__(self):
                try:
                    object = next(self.iter)
                except StopIteration:
                    raise StopAsyncIteration
                return object
        return AIterator

class AioQueueTool:
    @classmethod
    async def enqueue_iter(cls, q, iter):
        for x in iter:
            await q.put(x)

    @classmethod
    async def dequeue_n_nowait(cls, queue, n):
        logger = FoxylibLogger.func_level2logger(cls.dequeue_n_nowait, logging.DEBUG)
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
    async def dequeue_n_timeout(cls, queue, n, timeout=None):
        logger = FoxylibLogger.func_level2logger(cls.dequeue_n_timeout, logging.DEBUG)

        item_first = await queue.get()
        item_list = [item_first]

        try:
            # logger.debug({"n": n})
            for i in range(n - 1):
                item = await asyncio.wait_for(queue.get(), timeout=timeout)
                item_list.append(item)
        except asyncio.TimeoutError:
            pass

        return item_list

    @classmethod
    async def items2enqueue_by_chunk(cls, queue, items_in, p):
        item_list_in = list(items_in)
        n = len(item_list_in)

        k = n // p

        for i in range(k):
            await queue.put(items_in[p * i:p * (i + 1)])

        item_list_out = item_list_in[p * k:]
        return item_list_out

    @classmethod
    def queue2is_valid_loop(cls, queue):
        return queue._loop == asyncio.events.get_event_loop()


class AioPipeline:
    @dataclass
    class Config:
        f_queue: Callable[[], asyncio.Queue] = None
        dequeue_chunksize: int = 1
        dequeue_timeout: Optional[float] = None

        @CacheManager.attach_cachedmethod(self2cache=lambda x: LRUCache(maxsize=2), )
        def queue(self):
            return self.f_queue()

        @classmethod
        def config_list2init(cls, config_list, size):
            if config_list is None:
                return [cls(f_queue=asyncio.Queue) for _ in range(size)]

            def config2init(config):
                if not config:
                    return cls(f_queue=asyncio.Queue)

                if config.f_queue is None:
                    config.f_queue = asyncio.Queue
                return config

            return lmap(config2init, config_list)

    @classmethod
    async def coros_list2pipelined(cls, coros_list, queue_list):
        logger = FoxylibLogger.func_level2logger(cls.coros_list2pipelined, logging.DEBUG)
        n = len(coros_list)
        assert_greater_equal(n, 1)

        assert_equal(len(queue_list), n - 1)
        for q in queue_list:
            assert_true(AioQueueTool.queue2is_valid_loop(q))

        tasks_list = [lmap(asyncio.create_task, coros) for coros in coros_list]

        await asyncio.gather(*tasks_list[0])
        logger.debug('{}/{} coros done'.format(1, n))

        for i in range(1, n):
            await queue_list[i - 1].join()
            logger.debug('{}/{} queue empty'.format(i, n - 1))

            for c in tasks_list[i]:
                c.cancel()

            logger.debug('{}/{} coros done'.format(i + 1, n))

    @classmethod
    async def funcs_list2pipelined(cls, funcs_list, queue_list=None):
        assert_true(funcs_list)
        n = len(funcs_list)
        if queue_list:
            assert_equal(len(queue_list), n-1)

        batches_producer = funcs_list[0]
        batches_list_after = [[lambda l: f(iter2singleton(l)) for f in funcs]
                              for funcs in funcs_list[1:]
                              ]
        batches_list = [batches_producer, *batches_list_after]

        config_list = [AioPipeline.Config(f_queue=lambda: queue_list[i] if queue_list else None)
                       for i in range(n - 1)]

        return await cls.batches_list2pipelined(batches_list, config_list=config_list)

    @classmethod
    async def batch_queue2coro_producer(cls, batch, queue_out):
        for item_out in batch():
            await queue_out.put(item_out)

    @classmethod
    async def batch_queues2coro_piper(cls, batch, config_in, queue_out):
        queue_in = config_in.queue()
        chunksize = config_in.dequeue_chunksize
        timeout = config_in.dequeue_timeout

        while True:
            item_list_in = await AioQueueTool.dequeue_n_timeout(queue_in, chunksize, timeout=timeout)
            items_out = batch(item_list_in)
            for item_out in items_out:
                await queue_out.put(item_out)

            AioTool.task_count2all_done(len(item_list_in), queue_in,)

    @classmethod
    async def batch_queue2coro_consumer(cls, batch, config):
        queue_in = config.queue()
        chunksize = config.dequeue_chunksize
        timeout = config.dequeue_timeout

        while True:
            item_list_in = await AioQueueTool.dequeue_n_timeout(queue_in, chunksize, timeout=timeout)
            IterTool.consume(batch(item_list_in))
            AioTool.task_count2all_done(len(item_list_in), queue_in,)


    @classmethod
    async def batches_list2pipelined(cls, batches_list, config_list=None,):
        logger = FoxylibLogger.func_level2logger(cls.batches_list2pipelined, logging.DEBUG)
        n = len(batches_list)

        config_list = cls.Config.config_list2init(config_list, n-1)
        assert_equal(len(config_list), n - 1)

        queue_list = [config.queue() for config in config_list]
        for q in queue_list:
            assert_true(AioQueueTool.queue2is_valid_loop(q))

        async def batch2coro_producer(batch):
            return await cls.batch_queue2coro_producer(batch, queue_list[0])

        async def batch_index2coro_piper(batch, i):
            return await cls.batch_queues2coro_piper(batch, config_list[i-1], queue_list[i], )

        async def batch2coro_consumer(batch):
            return await cls.batch_queue2coro_consumer(batch, config_list[-1])

        coros_producer = lmap(batch2coro_producer, batches_list[0])
        coros_list_piper = [[batch_index2coro_piper(batch, i)
                              for batch in batches_list[i]]
                             for i in range(1, n - 1)]
        coros_consumer = lmap(batch2coro_consumer, batches_list[-1])
        coros_list = [coros_producer, *coros_list_piper, coros_consumer]

        return await cls.coros_list2pipelined(coros_list, queue_list)

