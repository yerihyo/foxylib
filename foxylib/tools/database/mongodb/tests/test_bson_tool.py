from pprint import pprint
from unittest import TestCase

from bson import ObjectId

from foxylib.tools.database.mongodb.bson_tool import BsonTool


class TestBsonTool(TestCase):
    def test_01(self):
        b_in = {
            "_id": ObjectId("5692a15524de1e0ce2dfcfa3"),
            "name": "hello world",
        }

        ref = BsonTool.bson2json(b_in)
        hyp = {'_id': '5692a15524de1e0ce2dfcfa3', 'name': 'hello world'}


        # pprint(ref)
        self.assertEqual(ref, hyp)