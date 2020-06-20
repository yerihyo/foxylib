import logging
from itertools import chain

from bson import ObjectId
from future.utils import lmap
from pymongo import UpdateOne

from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts, DictTool
from foxylib.tools.datetime.datetime_tool import DatetimeTool, DatetimeUnit
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class MongoDBTool:
    class Field:
        _ID = "_id"

    @classmethod
    def doc2id_excluded(cls, doc):
        return DictTool.keys2excluded(doc, [cls.Field._ID])

    @classmethod
    def tz2now(cls, tz):
        dt_natural = DatetimeTool.tz2now(tz)
        dt_truncated = DatetimeTool.truncate(dt_natural, unit=DatetimeUnit.Value.MILLISEC)
        return dt_truncated

    @classmethod
    def list2key(cls, l):
        return ".".join(l)

    @classmethod
    def bson2json(cls, b_in):
        if b_in is None:
            return None

        j_out = {k: v if k != cls.Field._ID else str(v)
                 for k, v in b_in.items()}
        return j_out

    # @classmethod
    # def result2j_doc_iter(cls, find_result):
    #     yield from map(cls.bson2json, find_result)

    # @classmethod
    # def j_pair2operation_upsertone(cls, j_pair, ):
    #     logger = FoxylibLogger.func_level2logger(cls.j_pair2operation_upsertone, logging.DEBUG)
    #     j_filter, j_update = j_pair
    #
    #     return UpdateOne(j_filter, {"$set": j_update}, upsert=True, )
    #
    # @classmethod
    # def j_pair_list2upsert(cls, collection, j_pair_list,):
    #     logger = FoxylibLogger.func_level2logger(cls.j_pair_list2upsert, logging.DEBUG)
    #
    #     op_list = cls.j_pair2operation_upsertone(j_pair_list)
    #     # bulk_write = ErrorTool.log_when_error(collection.bulk_write, logger)
    #     return collection.bulk_write(op_list)

    @classmethod
    def j_pair_list2upsert(cls, collection, j_pair_list, ):
        logger = FoxylibLogger.func_level2logger(cls.j_pair_list2upsert, logging.DEBUG)

        # def j_pair2operation_upsertone(j_pair, ):
        #     j_filter, j_update = j_pair
        #     return UpdateOne(j_filter, {"$set": j_update}, upsert=True, )

        op_list = [UpdateOne(j_filter, {"$set": j_update}, upsert=True, )
                   for j_filter, j_update in j_pair_list]

        # op_list = lmap(j_pair2operation_upsertone, j_pair_list)
        # bulk_write = ErrorTool.log_when_error(collection.bulk_write, logger)
        return collection.bulk_write(op_list)

    @classmethod
    def doc2id(cls, doc): return doc[cls.Field._ID]

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
        h = merge_dicts([{MongoDBTool.doc2id(j_doc): j_doc} for j_doc in j_doc_iter],
                        vwrite=vwrite_no_duplicate_key)
        return h


# class MongoDBAggregate:
#     class Field:
#         OK = "ok"
#         RESULT = "result"
#
#     @classmethod
#     def aggregate2ok(cls, aggregate):
#         return aggregate[cls.Field.OK] == 1
#
#     @classmethod
#     def aggregate2result(cls, aggregate):
#         return aggregate[cls.Field.RESULT]


class DocumentsDiff:
    class Field:
        FROM_ONLY = "from_only"
        TO_ONLY = "to_only"
        MISMATCHING = "mismatching"


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




