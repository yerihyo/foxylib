import copy
import inspect
import logging
from dataclasses import fields, asdict, make_dataclass, _FIELDS, replace, dataclass
from functools import reduce
from typing import TypeVar, Optional, get_type_hints

from dacite import from_dict, Type, Config, ForwardReferenceError, UnexpectedDataError, DaciteFieldError, \
    WrongTypeError, MissingValueError
from dacite.core import _build_value
from dacite.data import Data
from dacite.dataclasses import get_fields, get_default_value_for_field, DefaultValueNotFoundError, create_instance
from dacite.types import transform_value, is_instance
from future.utils import lmap, lfilter
from pipetools import pipe

from foxylib.tools.collections.collections_tool import DictTool, list2singleton, \
    merge_dicts
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool

T = TypeVar("T")

class DataclassTool:
    @classmethod
    def from_dict(cls, data_class: Type[T], data: Data, config: Optional[Config] = None) -> T:
        if data is None:
            return None

        return from_dict(data_class, data, config=config)

    @classmethod
    def dataobj2keys(cls, dataobj):
        return asdict(dataobj).keys()

    # @classmethod
    # @VersionTool.deprecated(reason="Use dataclass.asdict")
    # def to_dict(cls, dataobj_in) -> dict:
    #     dict_factory = pipe | dict | DictTool.emptyvalues2excluded
    #     return asdict(dataobj_in, dict_factory=dict_factory)

    @classmethod
    def asdict_cleaned(cls, dataobj_in:any) -> dict:
        dict_factory = pipe | dict | DictTool.emptyvalues2excluded
        return asdict(dataobj_in, dict_factory=dict_factory)

    @classmethod
    def dicts2dataobjs(cls, clazz, objs):
        dataobjs = [from_dict(clazz, obj) for obj in objs]
        return dataobjs

    @classmethod
    def dataobj2dict_clean(cls, dataobj):
        return DictTool.nullvalues2excluded(asdict(dataobj))

    @classmethod
    def replace_if_missing(cls, dataobj_in, key2is_missing=None, **changes_in):
        if key2is_missing is None:
            key2is_missing = lambda k: not bool(getattr(dataobj_in, k))

        keys_missing = lfilter(key2is_missing, changes_in.keys())
        changes_missing = DictTool.keys2filtered(changes_in, keys_missing)

        dataobj_out = replace(dataobj_in, **changes_missing)
        return dataobj_out
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
    def fieldname2checked(cls, dataclazz, fieldname: str) -> object:
        if cls.fieldname2is_valid(dataclazz, fieldname):
            return fieldname

        raise KeyError(fieldname)

    @classmethod
    def dict2fieldnames_checked(cls, dataclazz, dict_in: dict) -> object:
        fields_dataclazz = set(getattr(dataclazz, _FIELDS))
        fields_dict = set(dict_in.keys())

        if not (fields_dict <= fields_dataclazz):
            raise ValueError()

        return dict_in

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
    def schema2dataclass_tree(cls, classname, schema_in):
        def ktf2type_out(ktf):
            if isinstance(ktf[1], list):
                return cls.schema2dataclass_tree(ktf[0], ktf[1])
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

    @classmethod
    def merge(cls, objs, vwrite=None):
        clazz = list2singleton(lmap(type, objs))
        h_objs = lmap(lambda o: DictTool.nullvalues2excluded(asdict(o)), objs)
        h_out = merge_dicts(h_objs, vwrite=vwrite)
        obj_out = from_dict(clazz, h_out)
        return obj_out
