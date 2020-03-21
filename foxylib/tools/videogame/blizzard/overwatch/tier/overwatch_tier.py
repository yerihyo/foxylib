import os
from functools import lru_cache

from nose.tools import assert_true

from foxylib.tools.collections.collections_tool import filter2singleton, vwrite_no_duplicate_key, merge_dicts
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.json.json_tool import jdown
from foxylib.tools.json.yaml_tool import YAMLTool

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class OverwatchTier:
    class Value:
        BRONZE = "bronze"
        SILVER = "silver"
        GOLD = "gold"
        PLATINUM = "platinum"
        DIAMOND = "diamond"
        MASTER = "master"
        GRANDMASTER = "grandmaster"
        TOP500 = "top500"

    class Field:
        NAME = "name"
        IMAGE_URL = "image_url"
        VALUE = "value"


    @classmethod
    def skillrating2tier(cls, skillrating):
        assert_true(OverwatchSkillrating.skillrating2is_valid(skillrating))

        if skillrating < 1500:
            return cls.Value.BRONZE

        if skillrating < 2000:
            return cls.Value.SILVER

        if skillrating < 2500:
            return cls.Value.GOLD

        if skillrating < 3000:
            return cls.Value.PLATINUM

        if skillrating < 3500:
            return cls.Value.DIAMOND

        if skillrating < 4000:
            return cls.Value.MASTER

        return cls.Value.GRANDMASTER



    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def j_yaml(cls):
        filepath = os.path.join(FILE_DIR, "overwatch_tier.yaml")
        j = YAMLTool.filepath2j(filepath)
        return j

    @classmethod
    def j_list_all(cls):
        return cls.j_yaml()

    @classmethod
    def j2value(cls, j):
        return j[cls.Field.VALUE]

    @classmethod
    def j2image_url(cls, j):
        return j[cls.Field.IMAGE_URL]

    @classmethod
    def j_lang2name(cls, j, lang):
        return jdown(j, [cls.Field.NAME, lang])

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def h_value2j(cls):
        h = merge_dicts([{cls.j2value(j): j}
                     for j in cls.j_list_all()],
                    vwrite=vwrite_no_duplicate_key)
        return h

    @classmethod
    def value2j(cls, v):
        return cls.h_value2j().get(v)

    @classmethod
    def value_lang2name(cls, value, lang):
        j = cls.h_value2j(value)
        if not j:
            return None

        name = cls.j_lang2name(j, lang)
        return name


class OverwatchSkillrating:
    @classmethod
    def skillrating2is_valid(cls, skillrating):
        if skillrating is None:
            return True

        if not isinstance(skillrating, int):
            return False

        return 0 <= skillrating <= 5000
