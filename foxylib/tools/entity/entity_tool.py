class FoxylibEntity:
    class Field:
        SPAN = "span"
        VALUE = "value"
        TEXT = "text"
        # TYPE = "type"
    F = Field


    @classmethod
    def entity2span(cls, entity):
        # print({"j":j,}) # 'j["span"]':j["span"]})
        return entity[cls.Field.SPAN]

    @classmethod
    def entity2value(cls, entity):
        return entity[cls.Field.VALUE]

    # @classmethod
    # def entity2type(cls, entity):
    #     return entity.get(cls.Field.TYPE)

    @classmethod
    def entity2text(cls, entity):
        return entity.get(cls.Field.TEXT)
