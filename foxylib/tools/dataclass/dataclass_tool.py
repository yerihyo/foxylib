import inspect
import logging
from dataclasses import fields, asdict, make_dataclass, _FIELDS
from functools import reduce

from dacite import from_dict
from future.utils import lmap

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool


class DataclassTool:
    @classmethod
    @VersionTool.deprecated(reason="Use dacite.from_dict")
    def from_dict(cls, dataclass, data):
        return from_dict(dataclass, data)

    @classmethod
    @VersionTool.deprecated(reason="Use dataclass.asdict")
    def to_dict(cls, dataclass) -> dict:
        return asdict(dataclass)

    @classmethod
    def allfields2none(cls, dataobj):
        for f in fields(dataobj):
            setattr(dataobj, f.name, None)
        return dataobj

    @classmethod
    def fieldname2is_valid(cls, dataclazz, fieldname: str):
        fields = getattr(dataclazz, _FIELDS)
        return fieldname in fields

    @classmethod
    def fieldname2checked(cls, dataclazz, fieldname: str):
        if cls.fieldname2is_valid(dataclazz, fieldname):
            return fieldname

        raise KeyError(fieldname)


    @classmethod
    def dict2none_excluded(cls, h):
        return DictTool.filter(lambda k,v: v is not None, h)

    @classmethod
    def dict2empty_excluded(cls, h):
        return DictTool.filter(lambda k,v: not cls.value2is_empty(v), h)

    @classmethod
    def data2dict_noempty(cls, data):
        return DictTool.filter(lambda k, v: not cls.value2is_empty(v), asdict(data))

    @classmethod
    def value2is_empty(cls, v):
        if v is None:
            return True

        if v:
            return False

        if isinstance(v, (list, dict)):
            return True

        return False

    @classmethod
    def make_dataclass_recursive(cls, classname, schema_in):
        def ktf2type_out(ktf):
            if isinstance(ktf[1], list):
                return cls.make_dataclass_recursive(ktf[0], ktf[1])
            return ktf[1]

        def ktf2recursed(ktf_in):
            type_out = ktf2type_out(ktf_in)

            ktf_out = [ktf_in[0], type_out,]

            if len(ktf_in) > 2:
                ktf_out.append(ktf_in[2])

            return tuple(ktf_out)

        schema_out = lmap(ktf2recursed, schema_in)
        dataclazz = make_dataclass(classname, schema_out)
        return dataclazz

    @classmethod
    def jpath2subdataclass(cls, dataclass_in, jpath):
        def stepdown(dc, jstep):
            return dc.__annotations__[jstep]

        dataclass_out = reduce(stepdown, jpath, dataclass_in)
        return dataclass_out

    @classmethod
    def dataclass2fieldnames(cls, dataclazz):
        return set(inspect.signature(dataclazz).parameters)

    @classmethod
    def json2filtered(cls, dataclazz, data_in):
        logger = FoxylibLogger.func_level2logger(
            cls.json2filtered, logging.DEBUG)

        logger.debug({'data_in':data_in})

        fieldnames = cls.dataclass2fieldnames(dataclazz)

        data_out = DictTool.keys2filtered(data_in, fieldnames)
        return data_out

