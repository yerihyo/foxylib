import logging
from unittest import TestCase

from bson import ObjectId

from foxylib.tools.collections.iter_tool import iter2singleton
from future.utils import lmap
from pymongo import InsertOne, UpdateOne, MongoClient

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.database.mongodb.tests.foxylib_mongodb import FoxylibMongodb, MongodbToolCollection
from foxylib.tools.database.mongodb.mongodb_tool import DocumentTool, MongoDBTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibMongodb(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        c = MongodbToolCollection.collection_default()
        c.delete_many({})
        self.assertEqual(c.count({}), 0)

    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

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

    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_03, logging.DEBUG)

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

    def test_04(self):
        logger = FoxylibLogger.func_level2logger(self.test_04, logging.DEBUG)

        c = MongodbToolCollection.collection_default()
        c.delete_many({})

        client = MongoClient(host=FoxylibMongodb.uri())
        db = MongoDBTool.name2db(client, FoxylibMongodb.Constant.DBNAME)
        collection = MongodbToolCollection.db2collection(db)

        self.assertNotEqual(collection, c)



