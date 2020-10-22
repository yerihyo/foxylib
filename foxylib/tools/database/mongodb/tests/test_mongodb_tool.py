import logging
from decimal import Decimal
from pprint import pprint
from unittest import TestCase

from bson import Decimal128

from foxylib.tools.database.mongodb.mongodb_tool import MongoDBTool

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestMongodbTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        j_in = {"k1": Decimal("12.3"), "k2": [Decimal("1.1"), Decimal("2.3")]}
        hyp = MongoDBTool.json2bson(j_in)
        # pprint(hyp)

        ref = {"k1": Decimal128("12.3"),
               "k2": [Decimal128("1.1"), Decimal128("2.3")]}
        self.assertEqual(hyp, ref)
