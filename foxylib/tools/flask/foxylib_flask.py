import logging
import os
from functools import lru_cache, reduce

import connexion

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)





class FoxylibFlask:
    @classmethod
    def _load_urls2app(cls, app):
        logger = FoxylibLogger.func_level2logger(cls._load_urls2app, logging.DEBUG)

        # FlaskTool.add_url2app(app, url, view_func, )


    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def app(cls):
        logger = FoxylibLogger.func_level2logger(cls.app, logging.DEBUG)
        logger.debug({"START": "START"})

        application = connexion.FlaskApp(__name__, )
        # application.add_api('swagger.yaml', resolver=RestyResolver("ariana.main"))
        application.add_api('swagger.yaml')

        app = application.app
        j_config = {"STATIC_FOLDER":FoxylibFront.dirpath_static()}
        app.config.update(j_config)
        logger.debug({"app.static_folder": app.static_folder})

        cls._load_urls2app(app)

        logger.debug({"END": "END"})
        return app

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def test_client(cls):
        logger = FoxylibLogger.func_level2logger(cls.test_client, logging.DEBUG)
        logger.debug({"START": "START"})

        app = cls.app()
        c = app.test_client()

        logger.debug({"END": "END"})
        return c


    # @classmethod
    # @pytest.fixture
    # def client(cls):
    #     db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    #     flaskr.app.config['TESTING'] = True
    #
    #     with flaskr.app.test_client() as client:
    #         with flaskr.app.app_context():
    #             flaskr.init_db()
    #         yield client
    #
    #     os.close(db_fd)
    #     os.unlink(flaskr.app.config['DATABASE'])

class FoxylibFront:
    @classmethod
    def dirpath_static(cls):
        return os.path.join(FILE_DIR, "static")

    @classmethod
    def health_liveness(cls):
        return "Foxylib service is healthy based on liveness health check", 200

    @classmethod
    def health_readiness(cls):
        return "Foxylib service is healthy based on liveness health check", 200

    @classmethod
    def test_post(cls, k1, k2):
        return "Foxylib service is healthy based on liveness health check", 200



class FoxylibFlaskConfig:
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

def main():
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    app = FoxylibFlask.app()
    app.run()


if __name__ == '__main__':
    main() # python -m foxylib.tools.flask.foxylib_flask

