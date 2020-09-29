from dataclasses import fields


class DataclassTool:
    @classmethod
    def allfields2none(cls, obj):
        for f in fields(obj):
            setattr(obj, cls.field2name(f), None)
        return obj

    @classmethod
    def field2name(cls, field):
        return field.name


