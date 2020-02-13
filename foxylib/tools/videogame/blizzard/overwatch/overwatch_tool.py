from foxylib.tools.http.http_tool import HttpTool
from foxylib.tools.string.string_tool import format_str

from foxylib.tools.collections.collections_tool import lzip_strict

class BattletagTool:
    @classmethod
    def battletag2hyphened(cls, battletag):
        return battletag.replace("#","-")

# https://github.com/Fuyukai/OWAPI/blob/master/api.md
class OwapiTool:
    @classmethod
    def battletag2j_blob(cls, battletag):
        url = format_str("https://owapi.net/api/v3/u/{}/blob",
                         BattletagTool.battletag2hyphened(battletag))

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        kwargs = {"headers":{'User-Agent': user_agent}}
        httpr = HttpTool.url2httpr(url, kwargs=kwargs)
        j_blob = httpr.json()
        return j_blob


class OverwatchTool:
    @classmethod
    def battletag_test(cls):
        return "yeri#11211"