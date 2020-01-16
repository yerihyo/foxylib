import asyncio
import sys
from unittest import TestCase


class TestAsyncTool(TestCase):

    @classmethod
    @asyncio.coroutine
    def countdown_coroutine(cls, number, n):
        while n > 0:
            print("T-minus", n, "({})".format(number))
            yield from asyncio.sleep(1)
            n -= 1


    def test_01(self):
        cls = self.__class__

        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(cls.countdown_coroutine("A",2)),
                 asyncio.ensure_future(cls.countdown_coroutine("B", 3)),
                 ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        print("hello world", file=sys.stderr)



    @classmethod
    async def countdown_async(cls, number, n):
        while n > 0:
            print("T-minus", n, "({})".format(number))
            await asyncio.sleep(1)
            n -= 1


    def test_02(self):
        cls = self.__class__



        loop = asyncio.new_event_loop()
        futures = [cls.countdown_async("A", 2),
                   cls.countdown_async("B", 3),
                   ]
        loop.run_until_complete(asyncio.wait(futures))
        loop.close()  # ?? https://stackoverflow.com/questions/51271477/python3-x-runtimeerror-event-loop-is-closed

        print("hello world", file=sys.stderr)

    def test_03(self):
        cls = self.__class__

        async def countdown(number, n):
            while n>0:
                print("T-minus", n, "({})".format(number))
                await asyncio.sleep(1)
                n -= 1

        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(cls.countdown_async("A",2)),
                 asyncio.ensure_future(cls.countdown_async("B", 3)),
                 ]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

        print("hello world", file=sys.stderr)
