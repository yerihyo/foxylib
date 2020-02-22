import os
from functools import lru_cache

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
    V = Value

    class Field:
        NAME = "name"
        IMAGE_URL = "image_url"
        VALUE = "value"


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
