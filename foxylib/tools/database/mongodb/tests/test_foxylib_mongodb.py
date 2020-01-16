import logging
from unittest import TestCase

from future.utils import lmap

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.database.mongodb.foxylib_mongodb import FoxylibMongodb
from foxylib.tools.database.mongodb.mongodb_tool import DocumentTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibMongodb(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        db = FoxylibMongodb.db()
        c1 = db.get_collection("mongodb_tool")
        doc_list = list(c1.find({}))

        hyp1 = DictTool.dicts2keys(doc_list)
        ref1 = {'a', '_id', 'b'}
        self.assertEqual(hyp1, ref1)

    def test_02(self):
        db = FoxylibMongodb.db()
        c1 = db.get_collection("mongodb_tool")
        doc_list = list(c1.find({}))

        hyp = DictTool.dicts2keys(lmap(DocumentTool.doc2meta_keys_removed, doc_list))
        ref = {'a', 'b'}

        self.assertEqual(hyp, ref)

