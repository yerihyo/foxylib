import asyncio
import logging
from datetime import datetime, timedelta
from asyncio import ensure_future, gather, get_event_loop

import pytz
from aiostream.stream import merge
from nose.tools import assert_false

from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.datetime.datetime_tool import DatetimeTool, TimedeltaTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class AioTool:
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
    async def produce_consume(cls, queue2producer_list, queue2consumer_list):
        logger = FoxylibLogger.func_level2logger(cls.produce_consume, logging.DEBUG)

        queue = asyncio.Queue()

        # fire up the both producers and consumers
        producers = [asyncio.create_task(q2p(queue))
                     for q2p in queue2producer_list]
        consumers = [asyncio.create_task(q2c(queue))
                     for q2c in queue2consumer_list]

        # with both producers and consumers running, wait for
        # the producers to finish
        await asyncio.gather(*producers)
        logger.debug('producers done')

        # wait for the remaining tasks to be processed
        await queue.join()
        logger.debug('consumers done')

        # cancel the consumers, which are now idle
        for c in consumers:
            c.cancel()
        logger.debug('cancelled')
