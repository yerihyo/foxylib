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

        def subtest(loop):
            self.assertFalse(loop.is_closed())

            tasks = [asyncio.ensure_future(cls.countdown_coroutine("A",2), loop=loop),
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
    async def countdown_async(cls, number, n):
        while n > 0:
            print("T-minus", n, "({})".format(number))
            await asyncio.sleep(1)
            n -= 1


    def test_02(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())


            futures = [cls.countdown_async("A", 2),
                       cls.countdown_async("B", 3),
                       ]
            loop.run_until_complete(asyncio.wait(futures))
            print("hello world", file=sys.stderr)

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

            tasks = [asyncio.ensure_future(cls.countdown_async("A",2), loop=loop),
                     asyncio.ensure_future(cls.countdown_async("B", 3), loop=loop),
                     ]
            loop.run_until_complete(asyncio.gather(*tasks))

            print("hello world", file=sys.stderr)

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        # loop_system.close()  # do not close the loop if using asyncio.get_event_loop()

        loop_new = asyncio.new_event_loop()  # not working. closed when test closes
        subtest(loop_new)
        loop_new.close()  # can close because loop is from asyncio.new_event_loop()

