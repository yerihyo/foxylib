import json
import logging
import os
from functools import lru_cache, partial, reduce

from flask import session, render_template

from foxylib.tools.auth.auth0.auth0_tool import Auth0Tool
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.flask.flask_tool import FlaskTool
from foxylib.tools.flask.foxylib_flask import FoxylibFlask
from foxylib.tools.function.function_tool import FunctionTool, partial_n_wraps
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import URLTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*4, FILE_DIR)

class FoxyibFlaskConfigAuth0:
    # https://flask.palletsprojects.com/en/1.1.x/config/

    class Field:
        SESSION_TYPE = "SESSION_TYPE"
        SECRET_KEY = "SECRET_KEY"
        SECURITY_PASSWORD_SALT = "SECURITY_PASSWORD_SALT"
    F = Field

    @classmethod
    def j_config(cls):
        j = {cls.F.SESSION_TYPE: "filesystem",
             cls.F.SECRET_KEY: "sullivan_secret",
             cls.F.SECURITY_PASSWORD_SALT: "sullivan_secret second",
             }
        return j


class FoxylibAuth0:
    class Value:
        URL_LOGIN = "/auth0/login/"
    V = Value


    @classmethod
    def j_config(cls):
        j = {Auth0Tool.Config.API_BASE_URL: EnvTool.k2v("AUTH0_TENANT_URL"),
             Auth0Tool.Config.CLIENT_ID: EnvTool.k2v("AUTH0_CLIENT_ID"),
             Auth0Tool.Config.CLIENT_SECRET: EnvTool.k2v("AUTH0_CLIENT_SECRET"),
             }
        return j

    @classmethod
    def index(cls):
        filepath = os.path.join(FILE_DIR, "index.html")
        return Jinja2Tool.tmplt_file2html(filepath,)

    @classmethod
    def _load_urls2app(cls, app, auth0):
        logger = FoxylibLogger.func_level2logger(cls._load_urls2app, logging.DEBUG)

        callback_url = "/auth0/callback"
        FlaskTool.add_url2app(app, callback_url, partial_n_wraps(Auth0Tool.auth02callback,auth0),)

        FlaskTool.add_url2app(app, cls.V.URL_LOGIN,
                              partial_n_wraps(Auth0Tool.auth0_callback_url2login,auth0, "http://localhost:5000{}".format(callback_url)),)
        FlaskTool.add_url2app(app, "/dashboard/", cls.dashboard, )
        FlaskTool.add_url2app(app, "/", cls.index, )

    @classmethod
    # @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def add_auth02app(cls, app):
        app.config.update(FoxyibFlaskConfigAuth0.j_config())
        auth0 = Auth0Tool.flask_app2auth0(app, cls.j_config())
        cls._load_urls2app(app, auth0)
        return app


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
    app = FoxylibAuth0.add_auth02app(FoxylibFlask.app())
    app.run()


if __name__ == '__main__':
    main() # python -m foxylib.tools.auth.auth0.foxylib_auth0

