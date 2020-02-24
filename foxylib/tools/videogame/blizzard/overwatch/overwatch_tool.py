import requests
from future.utils import lmap, lfilter

from foxylib.tools.http.http_tool import HttpTool, HttprTool
from foxylib.tools.json.json_tool import JsonTool, jdown
from foxylib.tools.native.native_tool import is_not_none
from foxylib.tools.string.string_tool import format_str

from foxylib.tools.collections.collections_tool import lzip_strict, list2singleton


class BattletagTool:
    @classmethod
    def battletag2hyphened(cls, battletag):
        return battletag.replace("#","-")

    @classmethod
    def battletag2norm(cls, battletag):
        return battletag.replace("-", "#")


class OverwatchRole:
    class Value:
        TANK = "tank"
        SUPPORT = "support"
        DAMAGE = "damage"
    V = Value

# https://github.com/Fuyukai/OWAPI/blob/master/api.md
class OwapiTool:
    @classmethod
    def url2j(cls, url):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        kwargs = {"headers": {'User-Agent': user_agent}}
        httpr = HttpTool.url2httpr(url, kwargs=kwargs)
        if not HttprTool.httpr2is_ok(httpr):
            return None

        j = httpr.json()
        return j

    @classmethod
    def battletag2exists(cls, battletag):
        url = format_str("https://owapi.net/api/v3/u/{}/blob",
                         BattletagTool.battletag2hyphened(battletag))

        httpr = requests.head(url)
        # httpr = HttpTool.url2httpr(url)

        return HttprTool.httpr2is_ok(httpr)

    @classmethod
    def battletag2j_blob(cls, battletag):
        url = format_str("https://owapi.net/api/v3/u/{}/blob",
                         BattletagTool.battletag2hyphened(battletag))
        return cls.url2j(url)

    @classmethod
    def battletag2j_stats(cls, battletag):
        url = format_str("https://owapi.net/api/v3/u/{}/stats",
                         BattletagTool.battletag2hyphened(battletag))
        return cls.url2j(url)

    @classmethod
    def battletag2j_achievements(cls, battletag):
        url = format_str("https://owapi.net/api/v3/u/{}/achievements",
                         BattletagTool.battletag2hyphened(battletag))
        return cls.url2j(url)

    @classmethod
    def battletag2j_heroes(cls, battletag):
        url = format_str("https://owapi.net/api/v3/u/{}/heroes",
                         BattletagTool.battletag2hyphened(battletag))
        return cls.url2j(url)

    @classmethod
    def _j_stats_jpaths2comprank(cls, j_stats, jpath_list):
        comprank_list = lfilter(is_not_none, map(lambda jpath: jdown(j_stats, jpath), jpath_list))
        if not comprank_list:
            return None

        return list2singleton(comprank_list)

    @classmethod
    def j_stats2tank_comprank(cls, j_stats):
        jpath_list = [["eu", "stats", "competitive", "overall_stats", "tank_comprank"],
                      ["us", "stats", "competitive", "overall_stats", "tank_comprank"],
                      ["kr", "stats", "competitive", "overall_stats", "tank_comprank"],
                      ]
        return cls._j_stats_jpaths2comprank(j_stats, jpath_list)

    @classmethod
    def j_stats2damage_comprank(cls, j_stats):
        jpath_list = [["eu", "stats", "competitive", "overall_stats", "damage_comprank"],
                      ["us", "stats", "competitive", "overall_stats", "damage_comprank"],
                      ["kr", "stats", "competitive", "overall_stats", "damage_comprank"],
                      ]
        return cls._j_stats_jpaths2comprank(j_stats, jpath_list)

    @classmethod
    def j_stats2support_comprank(cls, j_stats):
        jpath_list = [["eu", "stats", "competitive", "overall_stats", "support_comprank"],
                      ["us", "stats", "competitive", "overall_stats", "support_comprank"],
                      ["kr", "stats", "competitive", "overall_stats", "support_comprank"],
                      ]
        return cls._j_stats_jpaths2comprank(j_stats, jpath_list)

