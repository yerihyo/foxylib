import logging
from decimal import Decimal
from pprint import pprint
from unittest import TestCase

from bson import Decimal128, ObjectId
from future.utils import lmap
from pymongo import InsertOne, UpdateOne, MongoClient, WriteConcern, \
    ReadPreference
from pymongo.read_concern import ReadConcern

from foxylib.tools.collections.iter_tool import iter2singleton
from foxylib.tools.database.mongodb.mongodb_tool import DocumentTool, \
    MongoDBTool
from foxylib.tools.database.mongodb.tests.foxylib_mongodb import FoxylibMongodb, \
    MongodbToolCollection
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestMongodbTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        j_in = {"k1": Decimal("12.3"), "k2": [Decimal("1.1"), Decimal("2.3")]}
        hyp = MongoDBTool.dict2bson(j_in)
        # pprint(hyp)

        ref = {"k1": Decimal128("12.3"),
               "k2": [Decimal128("1.1"), Decimal128("2.3")]}
        self.assertEqual(hyp, ref)

    def test_02(self):
        c = MongodbToolCollection.collection_default()
        c.delete_many({})
        self.assertEqual(c.count({}), 0)

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_03, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        doc_in = {'a': 'a', 'b': 'b'}
        op_list = [InsertOne(doc_in),
                   ]
        c.bulk_write(op_list)

        doc_found = iter2singleton(c.find({}))
        # hyp1 = DictTool.keys2excluded(doc_found, [MongoDBTool.Field._ID])
        logger.debug({"doc_found":doc_found, "doc_in":doc_in})
        self.assertEqual(doc_found, doc_in)

        self.assertTrue(isinstance(doc_in[MongoDBTool.Field._ID], ObjectId))  # doc_in updated!!
        self.assertTrue(isinstance(doc_found[MongoDBTool.Field._ID], ObjectId))

        hyp3 = set(doc_found.keys())
        ref3 = {'a', '_id', 'b'}
        self.assertEqual(hyp3, ref3)

    def test_04(self):
        logger = FoxylibLogger.func_level2logger(self.test_04, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        doc_in = {'a': 'a', 'b': 'b'}
        doc_upsert = {'b': 'c'}
        op_list = [InsertOne(doc_in),
                   UpdateOne({'a': 'a'}, {"$set":doc_upsert}, upsert=True),
                   ]
        c.bulk_write(op_list)

        self.assertEqual(c.count({}), 1)
        doc_found = iter2singleton(c.find({}))
        logger.debug({"doc_found": doc_found, "doc_in": doc_in, "doc_upsert":doc_upsert,})

        self.assertNotEqual(doc_found, doc_in)

        self.assertEqual(DocumentTool.doc2meta_keys_removed(doc_found), {"a": "a", "b": "c"})

        # hyp = DictTool.dicts2keys(lmap(DocumentTool.doc2meta_keys_removed, doc_list))
        # ref = {'a', 'b'}
        #
        # self.assertEqual(hyp, ref)

    def test_05(self):
        logger = FoxylibLogger.func_level2logger(self.test_05, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        client = MongoClient(host=FoxylibMongodb.uri())
        db = MongoDBTool.name2db(client, FoxylibMongodb.Constant.DBNAME)
        collection = MongodbToolCollection.db2collection(db)

        self.assertNotEqual(collection, c)

    def test_06(self):
        """
        test if InsertOne and UpdateOne can be under a single session
        :return:
        """
        logger = FoxylibLogger.func_level2logger(self.test_06, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        client = MongoClient(host=FoxylibMongodb.uri())
        with client.start_session() as session:
            def callback(_session):
                db = FoxylibMongodb.client2db(_session.client)
                ops = [InsertOne({"key": "x", "count": 3}),
                       UpdateOne({"key": "x"}, {"$inc": {"count": 2}}),
                       ]
                MongodbToolCollection.db2collection(db).bulk_write(ops)

            session.with_transaction(
                callback,
                read_concern=ReadConcern('local'),
                write_concern=WriteConcern("majority", wtimeout=1000),
                read_preference=ReadPreference.PRIMARY
            )

        hyp = lmap(MongoDBTool.doc2id_excluded, c.find({}))
        ref = [{'count': 5, 'key': 'x'}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_07(self):
        """
        test if unexisting field can be created if defined on path
        :return:
        """
        logger = FoxylibLogger.func_level2logger(self.test_07, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        c.insert_one({"key": "x"})
        c.update_one({"key": "x"},
                     {"$set": {"a.b.c": 1},
                      "$setOnInsert": {"d.e": 1},
                      },
                     upsert=True)

        hyp = lmap(MongoDBTool.doc2id_excluded, c.find({}))
        ref = [{'a': {'b': {'c': 1}}, 'key': 'x'}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_08(self):
        logger = FoxylibLogger.func_level2logger(self.test_08, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        key = lambda x: (x["_id"]["program_id"], x["_id"]["round_id"])

        docs = [
            {"program_id": 1, "extra": {"round_id": 'a', "user_key": "abc"}},
            {"program_id": 1, "extra": {"round_id": 'b', "user_key": "jkl"}},
            {"program_id": 1, "extra": {"round_id": 'b', "user_key": "xyz"}},
            {"program_id": 1, "extra": {"round_id": 'c', "user_key": "abc"}},
            {"program_id": 1, "extra": {"round_id": 'c', "user_key": "xyz"}},
            {"program_id": 1, "extra": {"round_id": 'c', "user_key": "xyz"}},
            {"program_id": 2, "extra": {"round_id": 'c', "user_key": "xyz"}},
            ]
        c.insert_many(docs)

        hyp1 = sorted(c.aggregate([
            {"$match": {"program_id": 1}},
            {"$group":
                 {"_id": {"round_id": "$extra.round_id",
                          "program_id": "$program_id"},
                  "user_keys": {"$addToSet": "$extra.user_key"},  # $addToSet
                  },
             },
            {"$unwind": "$user_keys"},
            {"$group":
                {"_id": "$_id",
                 "user_key_count": {"$sum": 1},
                 },
            },
        ]), key=key)
        ref1 = [
            {'_id': {'program_id': 1, 'round_id': 'a'}, 'user_key_count': 1},
            {'_id': {'program_id': 1, 'round_id': 'b'}, 'user_key_count': 2},
            {'_id': {'program_id': 1, 'round_id': 'c'}, 'user_key_count': 2},
        ]

        # pprint(hyp1)
        self.assertEqual(hyp1, ref1)

        hyp2 = sorted(c.aggregate([
            {"$match": {"program_id": 1}},
            {"$group":
                 {"_id": {"round_id": "$extra.round_id",
                          "program_id": "$program_id"},
                  "user_keys": {"$push": "$extra.user_key"},  # $push
                  },
             },
            {"$unwind": "$user_keys"},
            {"$group":
                 {"_id": "$_id",
                  "user_key_count": {"$sum": 1},
                  },
             },
        ]), key=key)
        ref2 = [
            {'_id': {'program_id': 1, 'round_id': 'a'}, 'user_key_count': 1},
            {'_id': {'program_id': 1, 'round_id': 'b'}, 'user_key_count': 2},
            {'_id': {'program_id': 1, 'round_id': 'c'}, 'user_key_count': 3},
        ]

        # pprint(hyp2)
        self.assertEqual(hyp2, ref2)

    def test_09(self):
        logger = FoxylibLogger.func_level2logger(self.test_09, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        key = lambda x: (x["_id"]["program_id"], x["_id"]["round_id"])

        docs = [
            {"k1": "k1",
             "l1": [{
                 "k2": "l1.k2",
                 "l2": [{"k3": "l1.l2.k3", "a": 1, 'b': 2}]
             }]
             },
            ]
        c.insert_many(docs)

        op = UpdateOne(
            {"k1":"k1", "l1.k2": "l1.k2"},
            {"$inc": {"l1.$[x1].l2.$[x2].b": 3},
             "$set": {"l1.$[x1].l2.$[x2].c": 'x'},
             },
            array_filters=[{'x1.k2': 'l1.k2'}, {'x2.k3': 'l1.l2.k3'}],
        )
        c.bulk_write([op])

        hyp = lmap(MongoDBTool.doc2id_excluded, c.find({}))
        ref = [
            {"k1": "k1",
             "l1": [{
                 "k2": "l1.k2",
                 "l2": [{"k3": "l1.l2.k3", "a": 1, 'b': 5, 'c':'x'}]
             }]
             },
        ]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_10(self):
        logger = FoxylibLogger.func_level2logger(self.test_10, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        docs = [{"k1": "k1", "l1": [{"k2": "l1.k2", }]},
                {"K1": "K1", "l1": []},
                ]
        c.insert_many(docs)

        op1 = UpdateOne(
            {"k1": "k1", "l1.k2": {"$ne": "l1.k2"}},
            {"$push": {"l1": {"k2": "l1.k2.invalid"}}, },
        )
        c.bulk_write([op1])

        hyp1 = lmap(MongoDBTool.doc2id_excluded, c.find({}))
        ref1 = [{'k1': 'k1', 'l1': [{'k2': 'l1.k2'}]}, {'K1': 'K1', 'l1': []}]

        # pprint(hyp1)
        self.assertEqual(hyp1, ref1)

        op2 = UpdateOne(
            {"k1": "k1", "l1.k2": {"$ne": "l1.k3"}},
            {"$push": {"l1": {"k2": "l1.k3"}}, },
        )
        c.bulk_write([op2])

        hyp2 = lmap(MongoDBTool.doc2id_excluded, c.find({}))
        ref2 = [{'k1': 'k1', 'l1': [{'k2': 'l1.k2'}, {'k2': 'l1.k3'}]},
                {'K1': 'K1', 'l1': []}]

        # pprint(hyp2)
        self.assertEqual(hyp2, ref2)

    def test_11(self):
        logger = FoxylibLogger.func_level2logger(self.test_10, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        ops = [
            InsertOne({"key": 'k', "value": 1}),
            UpdateOne({"key":'k',}, {"$set":{"value":2}}),
        ]
        cops = {MongodbToolCollection: ops}

        MongoDBTool.callback2db_atomic(
            callback=lambda session: MongoDBTool.cops2db(
                session.client, FoxylibMongodb.client2db, cops),
            client=FoxylibMongodb.client(),
        )

        hyp = lmap(MongoDBTool.doc2id_excluded,
                   map(MongoDBTool.bson2dict, c.find({})))
        ref = [{'key': 'k', 'value': 2}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

