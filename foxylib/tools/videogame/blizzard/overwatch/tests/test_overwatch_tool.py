from asyncio import gather
from pprint import pprint
from unittest import TestCase

from foxylib.tools.asyncio.asyncio_tool import AsyncioTool


class TestOverwatchTool(TestCase):
    # def test_01(self):
    #     from overwatch import Overwatch
    #     overwatch = Overwatch(battletag="Okush#11324", mode="competitive")
    #     print(overwatch.playtime)

    def test_02(self):
        import asyncio, aiohttp
        from overwatch_api.core import AsyncOWAPI
        from overwatch_api.constants import PC, XBOX, PLAYSTATION

        client = AsyncOWAPI()

        profile = AsyncioTool.awaitable2result(client.get_profile("yeri#11211", platform=PC))

        tasks = [client.get_profile("Danielfrogs#2552", platform=PC),
                 client.get_stats("Danielfrogs#2552", platform=XBOX),
                 client.get_achievements("Danielfrogs#2552", platform=PLAYSTATION),
                 client.get_hero_stats("Danielfrogs#2552"),
                 ]
        result_list = AsyncioTool.coroutine_list2result_list(tasks)
        pprint(result_list)