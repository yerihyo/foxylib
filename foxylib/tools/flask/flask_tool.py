import logging

from flask import url_for

from foxylib.tools.collections.collections_tool import l_singleton2obj, merge_dicts, DictTool, vwrite_no_duplicate_key
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.json.json_tool import jpath_v2j, jdown
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class FlaskToolSessionType:
    class Value:
        FILESYSTEM = "filesystem"
    V = Value


class FlaskTool:
    @classmethod
    def func2endpoint(cls, func):
        return FunctionTool.func2fullpath(func)

    @classmethod
    def add_url2app(cls, app, url, view_func, methods, endpoint=None, ):
        logger = FoxylibLogger.func_level2logger(cls.add_url2app, logging.DEBUG)
        # if methods is None:
        #     methods = ['GET']

        if endpoint is None:
            endpoint = cls.func2endpoint(view_func)

        logger.debug({"url":url,"endpoint":endpoint})
        app.add_url_rule(url,
                         endpoint=endpoint,
                         view_func=view_func,
                         methods=methods
                         )

    @classmethod
    def func2url(cls, f, values=None):
        if values is None:
            values = {}

        return url_for(cls.func2endpoint(f), **values)

    @classmethod
    def user2username_authenticated(cls, user):
        if not user: return None
        if not cls.user2is_authenticated(user): return None
        return str(user.username)

    @classmethod
    def user2email_authenticated(cls, user):
        if not user: return None
        if not cls.user2is_authenticated(user): return None
        return str(user.email)

    @classmethod
    def user2is_authenticated(cls, user): return user and user.is_authenticated


    @classmethod
    def request2params(cls, request):
        if not request: return None
        return request.args

    @classmethod
    def request_key2param(cls, request, key):
        url_params = cls.request2params(request)
        if not url_params: return None

        return url_params.get(key)



class FormResult:
    class Field:
        IN = "in"
        DATA = "data"
        ERROR = "error"
    F = Field

    @classmethod
    def j_form2is_valid(cls, j_form):
        j_error = j_form.get(cls.F.ERROR)
        return not j_error
    @classmethod
    def j_form2j_data(cls, j_form):
        return j_form.get(cls.F.DATA)

    # @classmethod
    # def j_form2j_in(cls, j_form):
    #     return j_form.get(cls.F.IN)

    @classmethod
    def j_form2h_jinja2(cls, j_form):
        if not j_form:
            return None

        h_jinja2 = {k: {"value": v}
                    for k, v in j_form.items()
                    if v
                    }
        return h_jinja2

class FormTool:
    @classmethod
    def form_field2str(cls, form, field):
        l = form.getlist(field)
        if not l:
            return l
        return l_singleton2obj(l)

    @classmethod
    def form_field2str_list(cls, form, field):
        return form.getlist(field)

    # @classmethod
    # def form2j_in(cls, form):
    #     return {k:form.getlist(k) for k in form.keys()}

    @classmethod
    def form2j_form(cls, form):
        if not form:
            return form

        return DictTool.filter(lambda k,v:v, form.patch_data)


    @classmethod
    def funcs_errclass2j_data(cls, f_list, error_class):
        j_data_list = []
        j_error_list = []
        for f in f_list:
            try:
                j_data_list.append(f())
            except error_class as e:
                j_error_list.append(FormError.error2j(e))

        if j_error_list:
            h_error_merged = merge_dicts(j_error_list, vwrite=DictTool.VWrite.extend)
            raise error_class(h_error_merged)

        j_data = merge_dicts(j_data_list, vwrite=vwrite_no_duplicate_key)
        return j_data

class FormError(Exception):
    class Each:
        class Field:
            TEXT = "text"
        F = Field

    def __init__(self, j_error):
        self.j_error = j_error

    @classmethod
    def error2j(cls, e):
        return e.j_error

    @classmethod
    def fieldname_text2error(cls, fieldname, text):
        h = jpath_v2j([fieldname, cls.Each.Field.TEXT], text)
        return cls(h)



rq2params = FlaskTool.request2params
rq_key2param = FlaskTool.request_key2param