import logging
from operator import itemgetter as ig

from bson import ObjectId
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError

from foxylib.tools.collections.chunk_tool import ChunkTool
from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts
from foxylib.tools.error.error_tool import ErrorTool
from foxylib.tools.json.json_tools import JToolkit
from foxylib.tools.log.logger_tools import FoxylibLogger


class MongoDBTool:
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
    def result2j_doc_iter(cls, find_result):
        for h in find_result:
            j = {k: v if k != "_id" else str(v)
                 for k, v in h.items()}
            yield j

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

    @classmethod
    def j_pair_list2upsert(cls, collection, j_pair_list,):
        logger = FoxylibLogger.func_level2logger(cls.j_pair_list2upsert, logging.DEBUG)

        requests = [UpdateOne(j_filter, {"$set":j_update}, upsert=True, )
                    for j_filter, j_update in j_pair_list]

        bulk_write = ErrorTool.log_when_error(collection.bulk_write, logger)
        return bulk_write(requests)


    @classmethod
    def j_doc2id(cls, j_doc): return j_doc["_id"]

    @classmethod
    def doc_id2datetime(cls, doc_id): return ObjectId(doc_id).generation_time

    @classmethod
    def field_values2jq_in(cls, field, value_list):
        return {field:{"$in":value_list}}

    @classmethod
    def jq_list2or(cls, jq_list):
        return {"$or": jq_list}

    @classmethod
    def j_doc_iter2h_doc_id2j_doc(cls, j_doc_iter):
        h = merge_dicts([{MongoDBTool.j_doc2id(j_doc): j_doc} for j_doc in j_doc_iter],
                        vwrite=vwrite_no_duplicate_key)
        return h
# class BulkTool:
#     class Operation:
#         INSERT = 1
#         UPDATE = 2
#         REMOVE = 3
#     Op = Operation
#
#     @classmethod
#     def op_j2action(cls, bulk, operation, j):
#         if operation == cls.Op.INSERT:
#             bulk.insert(j)
#             return
#
#         if operation == cls.Op.UPDATE:
#             bulk.up
#     @classmethod
#     def bulk(cls, bulk, collection, op_j_list):
#         for op, j in op_j_list:
#             if op == cls.Op.INSERT: bulk.insert(j)
#
#         bulk = collection.initialize_unordered_bulk_op()
#         bulk.insert({user: "abc123", status: "A", points: 0})
#         bulk.insert({user: "ijk123", status: "A", points: 0})
#         bulk.insert({user: "mop123", status: "P", points: 0})
#         bulk.execute()

    # class Op:
    #     ALL = "$all"
# class CollectionToolkit:
#     @classmethod
#     def c8n_jj_list2mirror(cls, c8n, jj_list):
#         pass