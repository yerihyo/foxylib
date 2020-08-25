import os
from functools import lru_cache

from pymongo import MongoClient

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.database.mongodb.mongodb_tool import MongoDBTool
from foxylib.tools.function.function_tool import FunctionTool


class FoxylibMongodb:
    class Constant:
        DBNAME = "foxylib"

    @classmethod
    def uri(cls):
        return FoxylibEnv.key2value("MONGO_URI")

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def client(cls):
        return MongoClient(host=cls.uri())

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def db(cls):
        client = cls.client()
        return MongoDBTool.name2db(client, cls.Constant.DBNAME)


class MongodbToolCollection:
    class Constant:
        NAME = "mongodb_tool"

    @classmethod
    def db2collection(cls, db, *_, **__):
        c = db.get_collection(cls.Constant.NAME, *_, **__)
        return c

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def collection_default(cls):
        db = FoxylibMongodb.db()
        return cls.db2collection(db)

