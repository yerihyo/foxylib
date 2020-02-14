from asyncio import ensure_future, gather, get_event_loop

from nose.tools import assert_false

from foxylib.tools.collections.collections_tool import l_singleton2obj


class AsyncioTool:
    @classmethod
    def awaitable2result(cls, awaitable, *_, **__):
        return l_singleton2obj(cls.awaitable_list2result_list([awaitable], *_, **__))


    @classmethod
    def awaitable_list2result_list(cls, awaitables, loop=None):
        if loop is None:
            loop = get_event_loop()

        assert_false(loop.is_closed())

        task_list = [ensure_future(x, loop=loop) for x in awaitables]
        result_list = loop.run_until_complete(gather(*task_list))
        return result_list

