from functools import lru_cache

from pymongo import MongoClient


class MongoDBToolkit:
    @classmethod
    def args2client(cls, url, port):
        client = MongoClient(url, port)
        return client

    @classmethod
    @lru_cache(maxsize=4)
    def args2db(cls, url, port, dbname):
        client = MongoClient(url, port)
        db = client[dbname]
        return db

    @classmethod
    def args2c8n(cls, url, port, dbname, c8nname):
        client = MongoClient(url, port)
        db = client[dbname]
        c8n = db[c8nname]
        return c8n

    @classmethod
    def list2key(cls, l):
        return ".".join(l)

    # class Op:
    #     ALL = "$all"
# class CollectionToolkit:
#     @classmethod
#     def c8n_jj_list2mirror(cls, c8n, jj_list):
#         pass