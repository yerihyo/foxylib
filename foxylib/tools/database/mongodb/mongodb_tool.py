import logging

from foxylib.tools.collections.groupby_tool import dict_groupby_tree
from itertools import chain

from bson import ObjectId
from future.utils import lmap
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts, DictTool, lchain
from foxylib.tools.datetime.datetime_tool import DatetimeTool, DatetimeUnit
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class Bulkitem:
    class Field:
        COLLECTION = "collection"
        OPERATIONS = "operations"

    @classmethod
    def item2collection(cls, item):
        return item[cls.Field.COLLECTION]

    @classmethod
    def item2operations(cls, item):
        return item[cls.Field.OPERATIONS]

    @classmethod
    def items2bulk_update(cls, items):
        collection2item_list = dict_groupby_tree(items, [cls.item2collection])

        for collection, item_list in collection2item_list:
            operation_list = lchain(*map(cls.item2operations, item_list))
            yield collection.bulk_write(operation_list)



class BulkWriteResultTool:
    class Field:
        UPSERTED = "upserted"
        N_INSERTED = "nInserted"
        N_UPSERTED = "nUpserted"
        N_MATCHED = "nMatched"
        N_MODIFIED = "nModified"
        N_REMOVED = "nRemoved"

    @classmethod
    def result2raw(cls, result):
        raw = result.bulk_api_result
        """
        {'writeErrors': [], 'writeConcernErrors': [], 'nInserted': 0, 'nUpserted': 0, 'nMatched': 1, 'nModified': 0, 
        'nRemoved': 0, 'upserted': []}
        """
        return raw

    @classmethod
    def result2upserted(cls, result):
        return cls.result2raw(result).get(cls.Field.UPSERTED) or []

    @classmethod
    def result2count_inserted(cls, result):
        return cls.result2raw(result).get(cls.Field.N_INSERTED)

    @classmethod
    def result2count_matched(cls, result):
        return cls.result2raw(result).get(cls.Field.N_MATCHED)

    @classmethod
    def result2count_upsert_source(cls, result):
        counts = [cls.result2count_inserted(result),
                  cls.result2count_matched(result),
                  ]
        return sum(counts)

    @classmethod
    def result2json(cls, b_result):
        b_upserted_list = cls.result2upserted(b_result)
        if not b_upserted_list:
            return b_result

        def upserted2json(upserted_in):
            _id = MongoDBTool.Field._ID
            upserted_out = merge_dicts([upserted_in, {_id: str(upserted_in[_id])}],
                                       vwrite=DictTool.VWrite.overwrite)
            return upserted_out

        j_upserted_list = lmap(upserted2json, b_upserted_list)

        j_result = merge_dicts([b_result, {cls.Field.UPSERTED: j_upserted_list}],
                               vwrite=DictTool.VWrite.overwrite)
        return j_result


class MongoDBTool:
    class Field:
        _ID = "_id"

    @classmethod
    def doc2id_excluded(cls, doc):
        return DictTool.keys2excluded(doc, [cls.Field._ID])

    @classmethod
    def name2db(cls, client, db_name):
        return client[db_name]

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
    # def bulk_write_result2dict(cls, bulk_write_result):
    #     result_out = {"bulk_api_result": bulk_write_result.bulk_api_result,
    #                   "inserted_count": bulk_write_result.inserted_count,
    #                   "matched_count": bulk_write_result.matched_count,
    #                   "modified_count": bulk_write_result.modified_count,
    #                   "deleted_count": bulk_write_result.deleted_count,
    #                   "upserted_count": bulk_write_result.upserted_count,
    #                   "upserted_ids": lmap(str, bulk_write_result.upserted_ids),
    #                   }
    #     return result_out





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

        def j_pair2op(j_pair):
            j_filter, j_update = j_pair
            update = {"$set": j_update,
                      #"$setOnInsert": j_update,
                      }
            op = UpdateOne(j_filter, update, upsert=True, )
            return op
        op_list = lmap(j_pair2op, j_pair_list)
        logger.debug({"op_list":op_list})

        # op_list = lmap(j_pair2operation_upsertone, j_pair_list)
        # bulk_write = ErrorTool.log_when_error(collection.bulk_write, logger)
        try:
            result = collection.bulk_write(op_list)
        except BulkWriteError as e:
            print(e.details)
            raise e
        return result

    @classmethod
    def doc2id(cls, doc): return doc[cls.Field._ID]

    @classmethod
    def doc_id2datetime(cls, doc_id): return ObjectId(doc_id).generation_time

    @classmethod
    def field_values2jq_in(cls, field, value_list):
        return {field: {"$in": value_list}}

    @classmethod
    def jq_list2or(cls, jq_list):
        return {"$or": jq_list}

    @classmethod
    def j_doc_iter2h_doc_id2j_doc(cls, j_doc_iter):
        h = merge_dicts([{MongoDBTool.doc2id(j_doc): j_doc} for j_doc in j_doc_iter],
                        vwrite=vwrite_no_duplicate_key)
        return h


    @classmethod
    def query_null(cls):
        return {cls.Field._ID: {"$exists": False}}
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




