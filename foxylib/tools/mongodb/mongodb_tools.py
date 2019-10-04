from pymongo import MongoClient


class MongoDBToolkit:
    # @classmethod
    # def args2client(cls, url, port):
    #     client = MongoClient(url, port)
    #     return client
    #
    # @classmethod
    # @lru_cache(maxsize=4)
    # def args2db(cls, url, port, dbname):
    #     client = MongoClient(url, port)
    #     db = client[dbname]
    #     return db

    @classmethod
    def args2c8n(cls, host, port, username, password, dbname, c8nname):
        client = MongoClient(host,
                             port=port,
                             username=username,
                             password=password,
                             )
        db = client[dbname]
        c8n = db[c8nname]
        return c8n

    @classmethod
    def list2key(cls, l):
        return ".".join(l)

    @classmethod
    def find_result2json(cls, find_result):
        return [{k: v if k != "_id" else str(v) for k, v in h.items()}
                for h in find_result]

    @classmethod
    def update_result2json(cls, update_result):
        return {"acknowledged":update_result.acknowledged,
                "matched_count":update_result.matched_count,
                "modified_count":update_result.modified_count,
                # "raw_result":update_result.raw_result,
                "upserted_id":str(update_result.upserted_id),
                }

    @classmethod
    def delete_result2json(cls, delete_result):
        return {"acknowledged": delete_result.acknowledged,
                "deleted_count": delete_result.deleted_count,
                # "raw_result":update_result.raw_result,
                }

    # class Op:
    #     ALL = "$all"
# class CollectionToolkit:
#     @classmethod
#     def c8n_jj_list2mirror(cls, c8n, jj_list):
#         pass