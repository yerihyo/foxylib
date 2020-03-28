import inspect

from foxylib.tools.collections.collections_tool import l_singleton2obj


class InspectTool:
    @classmethod
    def variable2name(cls, var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        l = [var_name for var_name, var_val in callers_local_vars if var_val is var]
        return l_singleton2obj(l)
