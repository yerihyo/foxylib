from functools import lru_cache

from foxylib.tools.entity.entity_tool import FoxylibEntity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.locale.locale_tool import LocaleTool


class DayofweekEntity:
    class Config:
        class Field:
            LOCALE = "locale"

        @classmethod
        def config2locale(cls, config):
            return config.get(cls.Field.LOCALE)

    class Value:
        MONDAY = "monday"
        TUESDAY = "tuesday"
        WEDNESDAY = "wednesday"
        THURSDAY = "thursday"
        FRIDAY = "friday"
        SATURDAY = "saturday"
        SUNDAY = "sunday"
    V = Value

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def entity_type(cls):
        return FoxylibEntity.class2entity_type(cls)

    @classmethod
    def text2entity_list(cls, str_in, config=None):
        locale = cls.Config.config2locale(config)
        lang = LocaleTool.locale2lang(locale)
        if lang == "ko":
            from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo
            return DayofweekEntityKo.text2entity_list(str_in)

        raise NotImplementedError("Invalid lang: {}".format(lang))



