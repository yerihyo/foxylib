import json
import logging
import os
from functools import lru_cache, reduce

from dacite import from_dict
from flask import session

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.auth.auth0.application.regular_web_application.auth0_webapp_tool import \
    Auth0WebappTool
from foxylib.tools.flask.flask_tool import FlaskTool
from foxylib.tools.flask.foxylib_flask import FoxylibFlask, FoxylibFlaskConfig
from foxylib.tools.function.function_tool import FunctionTool, partial_n_wraps
from foxylib.tools.jinja2.jinja2_tool import Jinja2Renderer
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*4, FILE_DIR)


class FoxylibAuth0appWebapp:
    class Value:
        URL_LOGIN = "/auth0/login/"
        URL_CALLBACK = "/auth0/callback/"
        URL_DASHBOARD = "/dashboard/"
        AUTH0_SUBDOMAIN = "dev-8gnjw0rn"
    V = Value

    @classmethod
    def name(cls):
        return 'webapp'

    @classmethod
    def abspath2url(cls, abspath):
        return "http://localhost:5000{}".format(abspath)

    @classmethod
    def scope(cls):
        return " ".join(["openid", "profile", "email"])

    @classmethod
    def config(cls) -> Auth0WebappTool.Config:
        h = {'api_url_base': FoxylibEnv.key2value("AUTH0_DOMAIN"),
             'client_id': FoxylibEnv.key2value("AUTH0_CLIENT_ID"),
             'client_secret': FoxylibEnv.key2value("AUTH0_CLIENT_SECRET"),
             'scope': cls.scope(),
             }
        config = from_dict(Auth0WebappTool.Config, h)
        return config

    @classmethod
    def index(cls):
        filepath = os.path.join(FILE_DIR, "index.html")
        return Jinja2Renderer.htmlfile2markup(filepath,)

    @classmethod
    def auth02callback(cls, auth0):
        return Auth0WebappTool.auth0_url2callback(auth0, cls.V.URL_DASHBOARD)

    @classmethod
    def _load_urls2app(cls, app, auth0):
        logger = FoxylibLogger.func_level2logger(cls._load_urls2app, logging.DEBUG)

        # callback_url = "/auth0/callback"
        FlaskTool.add_url2app(app, cls.V.URL_CALLBACK, partial_n_wraps(cls.auth02callback,auth0), methods=["GET",])

        FlaskTool.add_url2app(app, cls.V.URL_LOGIN,
                              partial_n_wraps(Auth0WebappTool.auth0_callback_url2login,
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
    #     return Auth0WebappTool.app_config2auth0(app, cls.j_config())

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def app_auth0(cls):
        app = FoxylibFlask.app()
        app.config.update(FoxylibFlaskConfig.j_config())
        #auth0 = Auth0WebappTool.app_config2auth0(app, cls.j_config())
        auth0 = cls.app2auth0(app)
        cls._load_urls2app(app, auth0)
        return app, auth0

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def app2auth0(cls, app):
        return Auth0WebappTool.app_config2auth0(app, cls.config())

    @classmethod
    @Auth0WebappTool.requires_auth
    def dashboard(cls):
        data = {"userinfo": session['profile'],
                "userinfo_pretty": json.dumps(session['jwt_payload'], indent=2),
                }
        filepath = os.path.join(FILE_DIR, "dashboard.html")
        return Jinja2Renderer.htmlfile2markup(filepath, data=data)


def main():
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    app, auth0 = FoxylibAuth0appWebapp.app_auth0()
    # app = FoxylibFlask.app()
    # app.config.update(FoxylibFlaskConfig.j_config())
    # auth0 = FoxylibAuth0.app2auth0(app)
    # FoxylibAuth0._load_urls2app(app, auth0)
    app.run()


if __name__ == '__main__':
    main() # python -m foxylib.tools.auth.auth0.foxylib_auth0

