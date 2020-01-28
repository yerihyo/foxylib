class EntityConfig:
    class Field:
        LOCALE = "locale"
    F = Field

    @classmethod
    def j2locale(cls, j):
        if not j:
            return None

        return j.get(cls.F.LOCALE)



class Entity:
    class Field:
        SPAN = "span"
        VALUE = "value"
        TEXT = "text"
    F = Field

    @classmethod
    def j2span(cls, j):
        # print({"j":j,}) # 'j["span"]':j["span"]})
        return j[cls.F.SPAN]

