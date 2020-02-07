from foxylib.tools.collections.collections_tool import zip_strict, lzip_strict
from foxylib.tools.locale.locale_tool import LocaleTool

from foxylib.tools.json.json_tool import jdown


class OverwatchTool:
    @classmethod
    def tier_list(cls,):
        return ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Top500"]

    @classmethod
    def lang2tier_value_name_list(cls, lang):
        v_list = cls.tier_list()


        if not lang or lang == "en":
            return [(x,x) for x in v_list]

        if lang == "ko":
            name_list = ["브론즈","실버","골드","플래티넘","다이아몬드","마스터","그랜드마스터","랭커"]
            return lzip_strict(v_list, name_list)

        raise NotImplementedError({"lang":lang})


