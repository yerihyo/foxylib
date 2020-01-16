import os
from functools import lru_cache

from foxylib.tools.function.function_tool import FunctionTool


class FoxylibNaver:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def client_id(cls):
        return os.environ.get("NAVER_APP_ID")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def secret_id(cls):
        return os.environ.get("NAVER_SECRET_ID")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def foxytrixy_auth_token(cls):
        return os.environ.get("NAVER_FOXYTRIXY_AUTH_TOKEN")
