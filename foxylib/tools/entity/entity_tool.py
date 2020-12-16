from foxylib.tools.native.clazz.class_tool import ClassTool
from foxylib.tools.span.indexspan_tool import IndexspanTool
from foxylib.tools.span.span_tool import SpanTool


class FoxylibEntity:
    class Field:
        TYPE = "type"
        SPAN = "span"
        VALUE = "value"

        # can have either or both
        FULLTEXT = "fulltext"
        TEXT = "text"

    @classmethod
    def class2entity_type(cls, clazz):
        return ClassTool.class2fullpath(clazz)

    @classmethod
    def entity2type(cls, entity):
        return entity[cls.Field.TYPE]

    @classmethod
    def entity2fulltext(cls, entity):
        return entity.get(cls.Field.FULLTEXT)

    @classmethod
    def entity2span(cls, entity):
        return entity[cls.Field.SPAN]

    @classmethod
    def entity2value(cls, entity):
        return entity[cls.Field.VALUE]

    @classmethod
    def entity2text(cls, entity):

        def fulltext2text(_entity):
            fulltext = cls.entity2fulltext(_entity)
            span = cls.entity2span(_entity)
            return IndexspanTool.list_span2sublist(fulltext, span)

        if cls.Field.TEXT not in entity:
            entity[cls.Field.TEXT] = fulltext2text(entity)

        return entity[cls.Field.TEXT]
