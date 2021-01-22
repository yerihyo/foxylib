import decimal
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from functools import lru_cache, wraps
from itertools import chain
from pprint import pformat
from typing import Callable

import pytz
from bson import ObjectId, Decimal128, Timestamp
from bson.decimal128 import create_decimal128_context
from future.utils import lmap
from nose.tools import assert_in
from pymongo import UpdateOne, InsertOne, WriteConcern, ReadPreference
from pymongo.errors import BulkWriteError
from pymongo.read_concern import ReadConcern

from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, \
    merge_dicts, DictTool, lchain, \
    l_singleton2obj, vwrite_overwrite
from foxylib.tools.collections.dicttree.dictschema_tool import \
    DictschemaTool
from foxylib.tools.collections.groupby_tool import dict_groupby_tree
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.collections.traversile.traversile_tool import TraversileTool
from foxylib.tools.datetime.datetime_tool import DatetimeTool, DatetimeUnit, \
    TimedeltaTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import is_not_none
from foxylib.tools.native.object_tool import ObjectTool
from foxylib.tools.span.interval_tool import IntervalTool


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


class InsertOneResultTool:
    @classmethod
    def result2j(cls, result):
        logger = FoxylibLogger.func_level2logger(cls.result2j, logging.DEBUG)

        j_raw = {'acknowledged': result.acknowledged,
                 'inserted_id': result.inserted_id,
                 }
        j_clean = DictTool.nullvalues2excluded(j_raw)
        j_out = MongoDBTool.bson2native(j_clean)

        # logger.debug(pformat({'j_out':j_out}))
        return j_out


class DeleteResultTool:
    # DeleteResult
    @classmethod
    def result2j(cls, result):
        raw_result = DictTool.keys2excluded(
            MongoDBTool.bson2native(result.raw_result),
            ['$clusterTime'],
        )

        j = {'raw_result': raw_result,
             'deleted_count': result.deleted_count,
             }
        return j


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


class MongoDBQueryvalue:
    @classmethod
    def array_not_empty(cls):
        return {"$exists": True, "$ne": []}


class MongoDBTool:
    class Field:
        _ID = "_id"

    @classmethod
    def datetime2utc(cls, dt):
        return DatetimeTool.as_utc(dt)

    @classmethod
    def result2json(cls, result_in):
        logger = FoxylibLogger.func_level2logger(cls.result2json, logging.DEBUG)

        j_raw = ObjectTool.object2dict(result_in)
        j_concise = DictTool.exclude_keys(j_raw, ['raw_result'])
        j_clean = DictTool.nullvalues2excluded(j_concise)
        j_out = MongoDBTool.bson2native(j_clean)

        return j_out



    # @classmethod
    # def find_one(cls, collection, native_in, *_, **__):
    #     result = collection.find_one(cls.native2bson(native_in), *_, **__)
    #     return result

    # @classmethod
    # def insert_one(cls, collection, native_in, *_, **__):
    #     result = collection.insert_one(cls.native2bson(native_in), *_, **__)
    #     # dict_out = merge_dicts([
    #     #     dict_in,
    #     #     {cls.Field._ID:result.inserted_id}
    #     # ], vwrite=vwrite_overwrite)
    #
    #     # j_result = InsertOneResultTool.result2j(result)
    #     return str(result.inserted_id)

    @classmethod
    def insert_one2bson(cls, collection, bson_in, *_, **__):
        logger = FoxylibLogger.func_level2logger(
            cls.insert_one2bson, logging.DEBUG)

        result = collection.insert_one(bson_in, *_, **__)
        bson_out = merge_dicts([
            bson_in,
            {cls.Field._ID: result.inserted_id}
        ], vwrite=vwrite_overwrite)
        return bson_out


    @classmethod
    def insert_one2native(cls, collection, native_in, converters_in, *_, **__):
        logger = FoxylibLogger.func_level2logger(
            cls.insert_one2native, logging.DEBUG)

        DictschemaTool.tree2typechecked(
            converters_in,
            {'bson2native': Callable,
             'native2bson': Callable,
             }
        )

        converters_out = merge_dicts([
            converters_in,
            {'bson2native': cls.bson2native, 'native2bson': cls.native2bson, },
        ], vwrite=DictTool.VWrite.skip_if_existing)

        bson2native = converters_out['bson2native']
        native2bson = converters_out['native2bson']

        bson_in = native2bson(native_in)
        logger.debug({'bson_in': bson_in})

        bson_out = cls.insert_one2bson(collection, bson_in)

        logger.debug({'bson_out':bson_out})
        native_out = bson2native(bson_out)
        return native_out

    @classmethod
    def interval2query_value_between(cls, interval,):
        point_start, point_end = interval
        s, s_inex = IntervalTool.Point.point2value_inex(point_start)
        e, e_inex = IntervalTool.Point.point2value_inex(point_end)

        h = {}
        if not IntervalTool.value2is_inf(s):
            gt = '$gte' if s_inex else '$gt'
            h[gt] = s

        if not IntervalTool.value2is_inf(e):
            lt = '$lte' if e_inex else '$lt'
            h[lt] = e

        if not h:
            return None

        return h

    @classmethod
    def interval_policy2comparator_pair(cls, interval_policy):

        inex_start, inex_end = IntervalTool.Policy.policy2clusivities(interval_policy)

        cmp_start = '$lte' if inex_start else '$lt'
        cmp_end = '$gte' if inex_end else '$gt'

        return cmp_start, cmp_end

        # query = {
        #     cls.Field.STARTS_AT: {"$lt": dt_pivot, },
        #     cls.Field.ENDS_AT: {"$gte": dt_pivot, },
        #
        # }

    @classmethod
    def collections2delete_all(cls, collections):
        for collection in collections:
            collection.delete_many({})

    @classmethod
    def value_or_exists_false(cls, v, f_true=None):
        if f_true is None:
            f_true = is_not_none

        if f_true(v):
            return v

        return {"$exists": False}

    @classmethod
    def id2oid(cls, id_in):
        return cls.id2ObjectId(id_in)

    @classmethod
    def id2ObjectId(cls, id_in):
        if isinstance(id_in, str):
            return ObjectId(id_in)

        if isinstance(id_in, ObjectId):
            return id_in

        raise NotImplementedError({"id_in": id_in})

    @classmethod
    def id2query(cls, id_in):
        return cls.ids2query([id_in])

    @classmethod
    def ids2query(cls, id_iterable):
        id_list = list(id_iterable)
        if not id_list:
            return {}

        oid_list = lmap(cls.id2ObjectId, id_list)
        if len(id_list) == 1:
            oid = l_singleton2obj(oid_list)
            return {cls.Field._ID: oid}

        query = {cls.Field._ID: {"$in": oid_list}}
        return query

    @classmethod
    def docs2query_ids(cls, docs):
        return cls.ids2query(map(cls.doc2id, docs))


    @classmethod
    def collection_doc2insert_one(cls, collection, doc):
        collection.insert_one(doc)
        assert_in("_id", doc)
        return doc

    @classmethod
    def doc2id_excluded(cls, doc):
        return DictTool.keys2excluded(doc, [cls.Field._ID])

    @classmethod
    def name2db(cls, client, db_name):
        return client[db_name]

    @classmethod
    def tz2now(cls, tz):
        dt_natural = DatetimeTool.tz2now(tz)
        dt_truncated = DatetimeTool.floor(dt_natural, unit=DatetimeUnit.MILLISECOND)
        return dt_truncated

    @classmethod
    def list2key(cls, l):
        return ".".join(l)

    @classmethod
    @lru_cache(maxsize=2)
    def decimal128_context(cls):
        return create_decimal128_context()

    @classmethod
    def bson_node2native(cls, b_in):
        if isinstance(b_in, ObjectId):
            return str(b_in)

        if isinstance(b_in, Timestamp):
            return b_in.time

        if isinstance(b_in, Decimal128):
            return Decimal(str(b_in))

        if isinstance(b_in, datetime):
            return DatetimeTool.astimezone(b_in, pytz.utc)

        return b_in

    @classmethod
    def bson2native(cls, b_in):
        logger = FoxylibLogger.func_level2logger(cls.bson2native, logging.DEBUG)

        if b_in is None:
            return None

        j_out = TraversileTool.tree2traversed(b_in, cls.bson_node2native,)
        return j_out

    @classmethod
    def native2bson(cls, h_in):
        if h_in is None:
            return None

        def native2bson_node(v):
            if isinstance(v, Decimal):
                with decimal.localcontext(cls.decimal128_context()) as ctx:
                    return Decimal128(ctx.create_decimal(str(v)))

            if isinstance(v, timedelta):
                return TimedeltaTool.timedelta2rune(v)

            return v

        pinpoint_tree = {cls.Field._ID: cls.id2oid}

        b_tmp = TraversileTool.tree2traversed(h_in, native2bson_node, )
        b_out = JsonTool.convert_pinpoint(b_tmp, pinpoint_tree)
        return b_out

    @classmethod
    def ids2dict_id2doc(cls, collection, ids):
        logger = FoxylibLogger.func_level2logger(
            cls.ids2dict_id2doc, logging.DEBUG)

        query = cls.ids2query(ids)
        # logger.debug({'ids': ids, 'query':query})

        docs = lmap(cls.bson2native, collection.find(query))

        h_id2doc = merge_dicts([{cls.doc2id(doc): doc} for doc in docs],
                               vwrite=vwrite_no_duplicate_key)

        return h_id2doc

    @classmethod
    def ids2docs(cls, collection, ids):
        h_id2doc = cls.ids2dict_id2doc(collection, ids)

        return [h_id2doc.get(str(id_)) for id_ in ids]

    @classmethod
    def id2doc(cls, collection, id):
        return IterTool.iter2singleton_or_none(cls.ids2docs(collection, [id]))


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

    @classmethod
    def _query_list2joined(cls, query_list, operator):
        if not query_list:
            return None

        if len(query_list) == 1:
            return query_list[0]

        return {operator: query_list}

    @classmethod
    def query_list2and(cls, query_list):
        return cls._query_list2joined(query_list, "$and")

    @classmethod
    def query_list2or(cls, query_list):
        return cls._query_list2joined(query_list, "$or")



    # @classmethod
    # def result2j_doc_iter(cls, find_result):
    #     yield from map(cls.bson2native, find_result)

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
    #     # bulk_write = ErrorTool.log_if_error(collection.bulk_write, logger)
    #     return collection.bulk_write(op_list)

    @classmethod
    def pair2operation_upsert(cls, j_filter, j_update):
        if not j_filter:
            return InsertOne(j_update)

        return UpdateOne(j_filter, {"$set": j_update}, upsert=True, )

    @classmethod
    def j_pair_list2upsert(cls, collection, j_pair_list, ):
        logger = FoxylibLogger.func_level2logger(cls.j_pair_list2upsert, logging.DEBUG)

        # def j_pair2operation_upsertone(j_pair, ):
        #     j_filter, j_update = j_pair
        #     return UpdateOne(j_filter, {"$set": j_update}, upsert=True, )

        op_list = lmap(lambda j_pair: cls.pair2operation_upsert(*j_pair), j_pair_list)
        logger.debug({"op_list":op_list})

        # op_list = lmap(j_pair2operation_upsertone, j_pair_list)
        # bulk_write = ErrorTool.log_if_error(collection.bulk_write, logger)
        try:
            result = collection.bulk_write(op_list)
        except BulkWriteError as e:
            print(e.details)
            raise e
        return result

    @classmethod
    def doc2id(cls, doc):
        return doc[cls.Field._ID]

    @classmethod
    def doc2oid(cls, doc):
        return cls.doc2object_id(doc)

    @classmethod
    def doc2object_id(cls, doc):
        id_ = cls.doc2id(doc)
        if isinstance(id_, ObjectId):
            return id_

        return ObjectId(id_)

    @classmethod
    def doc2id_str(cls, doc):
        return str(cls.doc2id(doc))

    @classmethod
    def docs2dict_id_str2doc(cls, docs):
        return merge_dicts([{cls.doc2id_str(doc): doc} for doc in docs],
                           vwrite=vwrite_no_duplicate_key)


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

    @classmethod
    def ops2db(cls, collection, ops):
        if not ops:
            return

        return collection.bulk_write(ops)

    @classmethod
    def func2callback(cls, func):
        def callback(session):  # not kwarg
            return func(session=session)  # kwarg
        return callback

    @classmethod
    def kwargs_transaction_default(cls):
        return {
            'read_concern': ReadConcern('local'),
            'write_concern': WriteConcern("majority", wtimeout=1000),
            'read_preference': ReadPreference.PRIMARY
        }

    @classmethod
    def callback2db_atomic(cls, callback, client, kwargs_transaction=None):
        logger = FoxylibLogger.func_level2logger(
            cls.callback2db_atomic, logging.DEBUG)

        if kwargs_transaction is None:
            kwargs_transaction = cls.kwargs_transaction_default()

        with client.start_session() as session_:
            return session_.with_transaction(
                lambda s: callback(session=s), **kwargs_transaction)


    # @classmethod
    # @ErrorTool.log_if_error
    # def cops2db(cls, client, client2db, cops, kwargs_transaction=None):
    #     logger = FoxylibLogger.func_level2logger(cls.cops2db, logging.DEBUG)
    #
    #     if kwargs_transaction is None:
    #         kwargs_transaction = {
    #             'read_concern': ReadConcern('local'),
    #             'write_concern': WriteConcern("majority", wtimeout=1000),
    #             'read_preference': ReadPreference.PRIMARY
    #         }
    #
    #     with client.start_session() as session:
    #         @IterTool.f_iter2f_list
    #         def callback(_session):
    #             db = client2db(_session.client)
    #
    #             for CollectionClass, ops in cops.items():
    #                 if not ops:
    #                     continue
    #                 # assert_true(ops, Collection)
    #
    #                 yield CollectionClass.db2collection(db).bulk_write(ops)
    #
    #         result = session.with_transaction(
    #             callback, **kwargs_transaction
    #         )
    #         return result

    # @classmethod
    # def session_cops2db(cls, session_, *_, **__):
    #     return cls.cops2db(session_.client, *_, **__)

    @classmethod
    @IterTool.f_iter2f_list
    def cops2db(cls, client, client2db, cops):
        logger = FoxylibLogger.func_level2logger(cls.cops2db, logging.DEBUG)

        db = client2db(client)
        for CollectionClass, ops in cops.items():
            if not ops:
                continue
            # assert_true(ops, Collection)

            yield CollectionClass.db2collection(db).bulk_write(ops)


class UpdateResult:
    class Field:
        MATCHED_COUNT = 'matched_count'
        MODIFIED_COUNT = 'modified_count'
        UPSERTED_ID = 'upserted_id'

    @classmethod
    def schema(cls):
        return {cls.Field.MATCHED_COUNT: int,
                cls.Field.MODIFIED_COUNT: int,
                cls.Field.UPSERTED_ID: str,
                }

    @classmethod
    def result2json(cls, result):
        return MongoDBTool.result2json(result)

    @classmethod
    def jpath2get(cls, result, jpath):
        return DictschemaTool.jpath2get(result, cls.schema(), jpath)

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




