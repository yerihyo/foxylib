from pprint import pformat

from future.utils import lfilter

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.function.function_tool import FunctionTool


class ObjectTool:
    @classmethod
    def obj2cls(cls, obj): return obj.__class__

    @classmethod
    def obj_name2has_variable(cls, obj, name):
        return name in obj.__dict__

    @classmethod
    def obj2dict(cls, obj):
        if hasattr(obj, "__slots__"):
            return cls.slotted2dict(obj)

        raise NotImplementedError()

    @classmethod
    def slotted2dict(cls, obj):
        return {s: getattr(obj, s) for s in obj.__slots__ if hasattr(obj, s)}

    @classmethod
    def field2is_public(cls, field):
        return not field.startswith('_')

    @classmethod
    def object2dict(cls, obj):
        fields = dir(obj)
        fields_public = lfilter(cls.field2is_public, fields)

        h_out = DictTool.filter(
            lambda k, v: not callable(v),
            {f: getattr(obj, f) for f in fields_public}
        )
        return h_out

        # h_out = {k:v
        #         for k,v in h_raw.items()}
        # raise Exception(pformat(h_out))

obj2cls = ObjectTool.obj2cls