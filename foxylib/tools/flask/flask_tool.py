import logging

from flask import url_for

from foxylib.tools.collections.collections_tool import l_singleton2obj, merge_dicts, DictTool, vwrite_no_duplicate_key
from foxylib.tools.function.function_tool import FunctionTool
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

    @classmethod
    def form_field2value(cls, form, field):
        l = form.getlist(field)
        if not l:
            return l
        return l_singleton2obj(l)

    # @classmethod
    # def form_error_list2merged(cls, h_error_list):
    #     h = merge_dicts(h_error_list, vwrite=DictTool.VWrite.extend)
    #     return h

    @classmethod
    def funcs_error2form_result(cls, f_list, error_class):
        h_result_list = []
        h_error_list = []
        for f in f_list:
            try:
                h_result_list.append(f())
            except error_class as e:
                h_error_list.append(e)

        if h_error_list:
            h_error_merged = merge_dicts(h_error_list, vwrite=DictTool.VWrite.extend)
            raise error_class(h_error_merged)

        h_result = merge_dicts(h_result_list, vwrite=vwrite_no_duplicate_key)
        return h_result



rq2params = FlaskTool.request2params
rq_key2param = FlaskTool.request_key2param