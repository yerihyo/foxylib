import json
import logging
import os
from functools import lru_cache, partial, reduce

from flask import session, render_template

from foxylib.tools.auth.auth0.auth0_tool import Auth0Tool
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.flask.flask_tool import FlaskTool
from foxylib.tools.flask.foxylib_flask import FoxylibFlask, FoxylibFlaskConfig
from foxylib.tools.function.function_tool import FunctionTool, partial_n_wraps
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import URLTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*4, FILE_DIR)

class FoxylibAuth0:
    class Value:
        URL_LOGIN = "/auth0/login/"
        URL_CALLBACK = "/auth0/callback/"
        URL_DASHBOARD = "/dashboard/"
        AUTH0_SUBDOMAIN = "dev-8gnjw0rn"
    V = Value

    @classmethod
    def abspath2url(cls, abspath):
        return "http://localhost:5000{}".format(abspath)

    @classmethod
    def scope(cls):
        return " ".join(["openid", "profile", "email"])

    @classmethod
    def j_config(cls):
        j = {Auth0Tool.Config.API_BASE_URL: EnvTool.k2v("AUTH0_TENANT_URL"),
             Auth0Tool.Config.CLIENT_ID: EnvTool.k2v("AUTH0_CLIENT_ID"),
             Auth0Tool.Config.CLIENT_SECRET: EnvTool.k2v("AUTH0_CLIENT_SECRET"),
             Auth0Tool.Config.SCOPE: cls.scope(),
             }
        return j

    @classmethod
    def index(cls):
        filepath = os.path.join(FILE_DIR, "index.html")
        return Jinja2Tool.tmplt_file2html(filepath,)

    @classmethod
    def auth02callback(cls, auth0):
        return Auth0Tool.auth0_url2callback(auth0, cls.V.URL_DASHBOARD)

    @classmethod
    def _load_urls2app(cls, app, auth0):
        logger = FoxylibLogger.func_level2logger(cls._load_urls2app, logging.DEBUG)

        # callback_url = "/auth0/callback"
        FlaskTool.add_url2app(app, cls.V.URL_CALLBACK, partial_n_wraps(cls.auth02callback,auth0), methods=["GET",])

        FlaskTool.add_url2app(app, cls.V.URL_LOGIN,
                              partial_n_wraps(Auth0Tool.auth0_callback_url2login,
                                              auth0,
                                              cls.abspath2url(cls.V.URL_CALLBACK),
                                              ),
                              methods=["GET", ]
                              )
        FlaskTool.add_url2app(app, cls.V.URL_DASHBOARD, cls.dashboard, methods=["GET",])
        # FlaskTool.add_url2app(app, "/", cls.index, )

    # @classmethod
    # @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    # def app2auth0(cls, app):
    #     return Auth0Tool.app_config2auth0(app, cls.j_config())

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def app_auth0(cls):
        app = FoxylibFlask.app()
        app.config.update(FoxylibFlaskConfig.j_config())
        #auth0 = Auth0Tool.app_config2auth0(app, cls.j_config())
        auth0 = cls.app2auth0(app)
        FoxylibAuth0._load_urls2app(app, auth0)
        return app, auth0

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def app2auth0(cls, app):
        return Auth0Tool.app_config2auth0(app, cls.j_config())

    @classmethod
    @Auth0Tool.requires_auth
    def dashboard(cls):
        data = {"userinfo": session['profile'],
                "userinfo_pretty": json.dumps(session['jwt_payload'], indent=2),
                }
        filepath = os.path.join(FILE_DIR, "dashboard.html")
        return Jinja2Tool.tmplt_file2html(filepath, data=data)


def main():
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    app, auth0 = FoxylibAuth0.app_auth0()
    # app = FoxylibFlask.app()
    # app.config.update(FoxylibFlaskConfig.j_config())
    # auth0 = FoxylibAuth0.app2auth0(app)
    # FoxylibAuth0._load_urls2app(app, auth0)
    app.run()


if __name__ == '__main__':
    main() # python -m foxylib.tools.auth.auth0.foxylib_auth0

