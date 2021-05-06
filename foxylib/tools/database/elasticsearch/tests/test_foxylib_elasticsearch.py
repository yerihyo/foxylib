import logging
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

import pytest
import pytz
from nose.tools import assert_false

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.database.elasticsearch.elasticsearch_tool import ElasticsearchTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.version.version_tool import VersionTool


class FoxylibElasticsearch:
    @classmethod
    def client(cls):
        raise NotImplementedError()


class UnittestIndex:
    @classmethod
    def env2name(cls, env):
        return "{}-unittest".format(env)

    @classmethod
    def settings(cls):
        # current settings of indexes
        settings = {
            "index": {
                "analysis": {
                    "filter": {
                        "english_snow": {
                            "type": "snowball",
                            "language": "English"
                        },
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        }
                    },
                    "analyzer": {
                        "english_analyzer": {
                            "filter": [
                                "standard",
                                "lowercase",
                                "english_snow",
                                "english_stop"
                            ],
                            "tokenizer": "standard"
                        }
                    }
                },
            }
        }
        return settings

    @classmethod
    def doc_type(cls):
        return "doc"

    @classmethod
    def mappings(cls):
        # current mappings of indexes (without prefix "mapping", "doc")

        mappings = {
            # "mapping": {
            cls.doc_type(): {
                "properties": {
                    "attribute_type": {
                        "type": "keyword"
                    },
                    "attribute_value": {
                        "type": "text",
                        "analyzer": "english_analyzer"
                    },
                    "created_at": {
                        "type": "date"
                    },
                    "updated_at": {
                        "type": "date"
                    },
                }
            }
            # }
        }
        return mappings



class TestNative(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @classmethod
    def index_init_unittest(cls, settings=None, mappings=None):
        logger = FoxylibLogger.func_level2logger(cls.index_init_unittest, logging.DEBUG)

        client = FoxylibElasticsearch.client()
        index = UnittestIndex.env2name(FoxylibEnv.env())
        logger.debug({"index_unittest": index})

        # ElasticsearchTool.delete_or_skip(client, index_unittest)

        # settings = UnittestIndex.settings()
        # mappings = UnittestIndex.mappings()

        body = DictTool.filter(lambda k, v: bool(v),
                               {"settings": settings if settings else None,
                                "mappings": mappings if mappings else None,
                                }
                               )
        ElasticsearchTool.create_or_skip(client, index, body=body)

        query_all = {"match_all": {}}
        client.delete_by_query(index, {"query": query_all}, refresh=True)

        result = client.search(index, body={"query": query_all, })
        assert_false(ElasticsearchTool.j_result2j_hit_list(result))

        return client, index

    @classmethod
    def doc2index_init(cls, doc, settings=None, mappings=None,):
        client, index = cls.index_init_unittest(settings=settings, mappings=mappings)
        client.index(index, UnittestIndex.doc_type(), doc, refresh="true")
        return client, index

    @classmethod
    @VersionTool.inactive(reason="Deleting index is not a good idea because Elasticsearch refuses "
                                 "deleting index when taking snapshot and test fails because of that.")
    def index_unittest_recreate(cls, client):
        logger = FoxylibLogger.func_level2logger(cls.index_unittest_recreate, logging.DEBUG)

        index_unittest = UnittestIndex.env2name(FoxylibEnv.env())
        logger.debug({"index_unittest": index_unittest})

        ElasticsearchTool.delete_or_skip(client, index_unittest)

        settings = UnittestIndex.settings()
        mappings = UnittestIndex.mappings()
        client.indices.create(index=index_unittest,
                              body={"settings": settings, "mappings": mappings})

    @classmethod
    def doc_default(cls, attribute_value):
        utc_now = datetime.now(tz=pytz.utc)
        attribute_type = 'size'

        doc = {'attribute_type': attribute_type,
               'attribute_value': attribute_value,
               'created_at': utc_now,
               'updated_at': utc_now,
               }
        return doc

    @pytest.mark.skip(reason="no Elasticsearch service ready for testing")
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        cls = self.__class__

        env = FoxylibEnv.env()
        logger.debug({"env": env})

        client, index_unittest = cls.index_init_unittest(settings=UnittestIndex.settings(),
                                                         mappings=UnittestIndex.mappings(),
                                                         )

        ref_mapping = """
        {
            'doc': {
                'properties': {
                    'attribute_type': {'type': 'keyword'},
                    'attribute_value': {'type': 'text', 'analyzer': 'english_analyzer'},
                    'created_at': {'type': 'date'},
                    'updated_at': {'type': 'date'}
                }
            }
        }
        """
        self.assertEqual(ElasticsearchTool.index2mapping(client, index_unittest),ref_mapping)

        ref_analysis = """
        {
            'analyzer': {
                'english_analyzer': {
                    'filter': ['standard',
                               'lowercase',
                               'english_snow',
                               'english_stop'],
                    'tokenizer': 'standard'
                }
            },
            'filter': {
                'english_snow': {
                    'language': 'English',
                    'type': 'snowball'
                },
                'english_stop': {
                    'stopwords': '_english_',
                    'type': 'stop'
                }
            }
        }
        """
        self.assertEqual(ElasticsearchTool.index2analysis(client, index_unittest),ref_analysis,)

    @pytest.mark.skip(reason="no Elasticsearch service ready for testing")
    def test_04(self):
        cls = self.__class__
        client, index_unittest = cls.doc2index_init(cls.doc_default('8'),
                                                    settings=UnittestIndex.settings(),
                                                    mappings=UnittestIndex.mappings(),
                                                    )

        query_1 = {"match_all": {}}
        result_1 = client.search(index_unittest, body={"query": query_1,})
        hits_1 = ElasticsearchTool.j_result2j_hit_list(result_1)
        self.assertEqual(len(hits_1), 1)  # there exists one document

        query_2 = {"term": {"attribute_value": "8"}}
        result_2 = client.search(index_unittest, body={"query": query_2})
        hits_2 = ElasticsearchTool.j_result2j_hit_list(result_2)
        self.assertEqual(len(hits_2), 1)  # "8" can be searched using "8"

        query_3 = {"term": {"attribute_value": 8}}  # integer query for text type
        result_3 = client.search(index_unittest, body={"query": query_3})
        hits_3 = ElasticsearchTool.j_result2j_hit_list(result_3)

        self.assertEqual(len(hits_3), 1)  # "8" can be searched using 8

    @pytest.mark.skip(reason="no Elasticsearch service ready for testing")
    def test_05(self):
        cls = self.__class__

        client, index_unittest = cls.doc2index_init(cls.doc_default(8),
                                                    settings=UnittestIndex.settings(),
                                                    mappings=UnittestIndex.mappings(),
                                                    )
        query_1 = {"match_all": {}}
        result_1 = client.search(index_unittest, body={"query": query_1,})
        hits_1 = ElasticsearchTool.j_result2j_hit_list(result_1)
        self.assertEqual(len(hits_1), 1)  # there exists one document

        query_2 = {"term": {"attribute_value": "8"}}
        result_2 = client.search(index_unittest, body={"query": query_2})
        hits_2 = ElasticsearchTool.j_result2j_hit_list(result_2)
        self.assertEqual(len(hits_2), 1, result_2)  # 8 can be searched using "8"

        query_3 = {"term": {"attribute_value": 8}}  # integer query for text type
        result_3 = client.search(index_unittest, body={"query": query_3})
        hits_3 = ElasticsearchTool.j_result2j_hit_list(result_3)
        self.assertEqual(len(hits_3), 1, result_3)  # 8 can be searched using 8

        query_4 = {"term": {"attribute_value": 8.0}}  # integer query for text type
        result_4 = client.search(index_unittest, body={"query": query_4})
        hits_4 = ElasticsearchTool.j_result2j_hit_list(result_4)
        self.assertEqual(len(hits_4), 0, result_4)  # 8 CANNOT be searched using 8.0

    @pytest.mark.skip(reason="no Elasticsearch service ready for testing")
    def test_06(self):
        cls = self.__class__

        client, index_unittest = cls.doc2index_init(cls.doc_default(8.0),
                                                    settings=UnittestIndex.settings(),
                                                    mappings=UnittestIndex.mappings(),
                                                    )
        query_1 = {"match_all": {}}
        result_1 = client.search(index_unittest, body={"query": query_1,})
        hits_1 = ElasticsearchTool.j_result2j_hit_list(result_1)
        self.assertEqual(len(hits_1), 1)  # there exists one document

        query_2 = {"term": {"attribute_value": "8"}}
        result_2 = client.search(index_unittest, body={"query": query_2})
        hits_2 = ElasticsearchTool.j_result2j_hit_list(result_2)
        self.assertEqual(len(hits_2), 0, result_2)  # 8.0 CANNOT be searched using "8"

        query_3 = {"term": {"attribute_value": 8}}  # integer query for text type
        result_3 = client.search(index_unittest, body={"query": query_3})
        hits_3 = ElasticsearchTool.j_result2j_hit_list(result_3)
        self.assertEqual(len(hits_3), 0, result_3)  # 8.0 CANNOT be searched using 8

        query_4 = {"term": {"attribute_value": 8.0}}  # integer query for text type
        result_4 = client.search(index_unittest, body={"query": query_4})
        hits_4 = ElasticsearchTool.j_result2j_hit_list(result_4)
        self.assertEqual(len(hits_4), 1, result_4)  # 8.0 CAN be searched using 8.0

        query_5 = {"term": {"attribute_value": "8.0"}}  # integer query for text type
        result_5 = client.search(index_unittest, body={"query": query_5})
        hits_5 = ElasticsearchTool.j_result2j_hit_list(result_5)
        self.assertEqual(len(hits_5), 1, result_5)  # 8.0 CAN be searched using "8.0"

        query_6 = {"term": {"attribute_value": "8.00"}}  # integer query for text type
        result_6 = client.search(index_unittest, body={"query": query_6})
        hits_6 = ElasticsearchTool.j_result2j_hit_list(result_6)
        self.assertEqual(len(hits_6), 0, result_6)  # 8.0 CANNOT be searched using "8.00"

        query_7 = {"term": {"attribute_value": Decimal("8.0")}}  # integer query for text type
        result_7 = client.search(index_unittest, body={"query": query_7})
        hits_7 = ElasticsearchTool.j_result2j_hit_list(result_7)
        self.assertEqual(len(hits_7), 1, result_7)  # 8.0 CAN be searched using Decimal("8.0")

        query_8 = {"term": {"attribute_value": Decimal("8.00")}}  # integer query for text type
        result_8 = client.search(index_unittest, body={"query": query_8})
        hits_8 = ElasticsearchTool.j_result2j_hit_list(result_8)
        self.assertEqual(len(hits_8), 1, result_8)  # 8.0 CAN be searched using Decimal("8.00")

    @pytest.mark.skip(reason="no Elasticsearch service ready for testing")
    def test_07(self):
        """
        Test bulk update
        :return:
        """
        client = GadgetElasticsearch.client()

        index_from = KontextProductIndex.index(
            "staging",
            FranchiseToolkit.name_env2franchise_id('carters', 'staging'))
        query = KontextProductIndex.query_product_reference()
        hits = KontextProductIndex.query2hits(client, index_from, query)

        index_to = KontextProductIndex.index(
            "dev",
            FranchiseToolkit.name_env2franchise_id('carters', 'dev'))
        KontextProductIndex.hits2replace_many_synonyms(client, hits, index_to)