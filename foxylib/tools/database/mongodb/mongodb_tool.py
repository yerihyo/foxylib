import logging
from itertools import chain

from bson import ObjectId
from future.utils import lmap, lfilter
from nose.tools import assert_in
from pymongo import MongoClient, UpdateOne, ASCENDING

from foxylib.tools.collections.chunk_tool import ChunkTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts, f_iter2f_list, DictTool, \
    sfilter
from foxylib.tools.error.error_tool import ErrorTool
from foxylib.tools.version.version_tool import VersionTool


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
    @VersionTool.deprecated(version_tos="v0.4")
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

class DocumentsDiff:
    class Field:
        FROM_ONLY = "from_only"
        TO_ONLY = "to_only"
        MISMATCHING = "mismatching"
    F = Field

class DocumentTool:
    @classmethod
    def key2is_underscored(cls, key):
        return key.startswith("_")

    @classmethod
    def meta_keys(cls):
        return {"_id","_created","_modified"}

    @classmethod
    def doc2meta_keys_removed(cls, doc):
        return DictTool.keys2excluded(doc, cls.meta_keys())


    @classmethod
    def docs_pair2j_diff(cls, docs_pair, keys=None):
        docs1, docs2 = docs_pair
        doc_list_1, doc_list_2 = list(docs1), list(docs2)
        n1, n2 = len(doc_list_1), len(doc_list_2)

        if keys is None:
            keys = DictTool.dicts2keys(chain(doc_list_1,doc_list_2))

        h2key = lambda h: tuple(h[k] for k in keys)
        h1 = merge_dicts([{h2key(h): h} for h in doc_list_1],
                         vwrite=vwrite_no_duplicate_key)

        key_list_1 = lmap(h2key, doc_list_1)
        key_list_2 = lmap(h2key, doc_list_2)

        key_set_1 = set(key_list_1)
        key_set_2 = set(key_list_2)






    # @classmethod
    # @f_iter2f_list
    # def collection_pair2diff_list(cls, c1, c2):
    #     docs1 = c1.find().sort("_id", ASCENDING)
    #     docs2 = c2.find().sort("_id", ASCENDING)
    #
    #     doc1 = next(docs1, None)
    #     doc2 = next(docs2, None)
    #
    #     def index_smaller2doc_pair_next(i):
    #         assert_in(i, [None,0,1])
    #
    #         if i is None:
    #             return (next(docs1, None), next(docs2,None))
    #         if i==0:
    #             return (next(docs1,None), doc2)
    #         if i==1:
    #             return (doc1, next(docs2, None))
    #
    #         raise RuntimeError("Should not come here! Invalid 'i': {}".format(i))
    #
    #     def index_smaller2diff(i, doc1, doc2):
    #         assert_in(i, [None, 0, 1])
    #         if i is None:
    #             return DocumentTool.doc_pair2diff(doc1, doc2)
    #         if i==0:
    #             return DocumentTool.doc2diff(doc1)
    #         if i==1:
    #             return DocumentTool.doc2diff(doc2)
    #         raise RuntimeError("Should not come here! Invalid 'i': {}".format(i))
    #
    #
    #     while (doc1 is not None) and (doc2 is not None):
    #         if doc1 is None:
    #             yield from map(DocumentTool.doc2diff, docs2)
    #             break
    #
    #         if doc2 is None:
    #             yield from map(DocumentTool.doc2diff, docs1)
    #             break
    #
    #         index_smaller = DocumentTool.doc_pair2index_smaller(doc1, doc2)
    #         assert_in(index_smaller, [None, 0, 1])
    #
    #         yield index_smaller2diff(index_smaller)
    #         doc1, doc2 = index_smaller2doc_pair_next(index_smaller)



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