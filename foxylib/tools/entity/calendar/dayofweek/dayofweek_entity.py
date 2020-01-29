from foxylib.tools.entity.entity_tool import EntityConfig
from foxylib.tools.locale.locale_tool import LocaleTool

from foxylib.tools.locale.locale_tool import LocaleTool


class DayofweekEntity:
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
    def str2entity_list(cls, str_in, j_config=None):
        locale = EntityConfig.j2locale(j_config)
        lang = LocaleTool.locale2lang(locale)
        if lang == "ko":
            from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo
            return DayofweekEntityKo.str2entity_list(str_in)

        raise NotImplementedError("Invalid lang: {}".format(lang))



