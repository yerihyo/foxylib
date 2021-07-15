import logging
import traceback
from functools import wraps

from flask import url_for, request
from werkzeug.datastructures import EnvironHeaders
from werkzeug.wrappers import BaseResponse

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
    def shutdown(cls):
        """
        https://stackoverflow.com/a/17053522
        :return:
        """
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @classmethod
    def wrapper_shutdown_on_error(cls, func):
        @wraps(func)
        def wrapped(*_, **__):
            try:
                return func(*_, **__)
            except:
                traceback.print_exc()
                cls.shutdown()

        return wrapped


    @classmethod
    def request2json_form(cls, request):
        """
        reference: https://stackoverflow.com/questions/45590988/converting-flask-form-data-to-json-only-gets-first-value
        """
        return request.form.to_dict(flat=False)

    @classmethod
    def response2never_cache(cls, response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.

        reference: https://stackoverflow.com/a/34067710/1902064
        """

        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        response.cache_control.max_age = 0


        # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        # response.headers["Pragma"] = "no-cache"
        # response.headers["Expires"] = "0"
        return response

    @classmethod
    def func2log_request(cls, func, logfunc):
        """
        request.headers is an EnvironHeaders object, which lacks `__dict__` function.
        Therefore, exploiting `__iter__` function instead.
        :param func:
        :param logfunc:
        :return:
        """
        @wraps(func)
        def wrapped(*_, **__):
            logfunc({'headers': {k: v for k, v in request.headers},
                     'json': request.json,
                     })
            return func(*_, **__)

        return wrapped

# rq2params = FlaskTool.request2params
# rq_key2param = FlaskTool.request_key2param
