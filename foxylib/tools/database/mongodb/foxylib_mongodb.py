import os
from functools import lru_cache

from pymongo import MongoClient

from foxylib.tools.function.function_tool import FunctionTool


class FoxylibMongodb:
    DBNAME = "foxylib"

    @classmethod
    def uri(cls): return os.environ.get("MONGO_URI")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def client(cls): return MongoClient(host=cls.uri())

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def db(cls):
        client = cls.client()
        return client[cls.DBNAME]
