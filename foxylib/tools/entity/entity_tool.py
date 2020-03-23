class EntityConfig:
    class Field:
        LOCALE = "locale"
    F = Field

    @classmethod
    def config2locale(cls, j):
        if not j:
            return None

        return j.get(cls.Field.LOCALE)



class Entity:
    class Field:
        SPAN = "span"
        VALUE = "value"
        TEXT = "text"
        TYPE = "type"
    F = Field


    @classmethod
    def entity2span(cls, entity):
        # print({"j":j,}) # 'j["span"]':j["span"]})
        return entity[cls.Field.SPAN]

    @classmethod
    def entity2value(cls, entity):
        return entity[cls.Field.VALUE]

    @classmethod
    def entity2type(cls, entity):
        return entity.get(cls.Field.TYPE)
