import logging
from itertools import chain
from pprint import pformat

from future.utils import lmap

from foxylib.tools.collections.collections_tool import merge_dicts, DictTool, lchain
from foxylib.tools.database.elasticsearch.elasticsearch_tool import ElasticsearchTool
from foxylib.tools.json.json_tool import JsonTool


class SampleIndex:
    @classmethod
    def query_product_reference(cls):
        return ElasticsearchTool.key_values2query_terms("attribute_type", ["product_reference"])

    @classmethod
    def query2hits(cls, client, index, query):
        results = ElasticsearchTool.search_scroll2result_iter(
            client,
            {"index": index,
             "body": {'query': query},
             "request_timeout": 3,
             },
            scroll="60s",
        )
        hits = chain.from_iterable(map(ElasticsearchTool.result2hits, results))
        return hits

    @classmethod
    def hit2v1(cls, hit):
        return JsonTool.down(hit, ['_source', 'v1'])

    @classmethod
    def hit2v2(cls, hit):
        return JsonTool.down(hit, ['_source', 'v2'])

    @classmethod
    def hits2replace_many_v2(cls, client, hits_in, index):
        dict_v1_to_v2 = merge_dicts([
            {cls.hit2v1(hit_in): cls.hit2v2(hit_in)} for hit_in in hits_in
        ], vwrite=DictTool.VWrite.no_duplicate_key)

        queries_values = [ElasticsearchTool.key_value2query_match("v1", v1) for v1 in dict_v1_to_v2.keys()]
        queries = [
            ElasticsearchTool.queries2should(queries_values),
            cls.query_product_reference(),
        ]
        query = ElasticsearchTool.queries2query_aggregated(queries, "must")
        hits = cls.query2hits(client, index, query)

        def hit2actions(hit):
            if not hit:
                return []

            v1 = cls.hit2v1(hit)
            v2 = dict_v1_to_v2.get(v1)
            if not v2:
                return []

            id_this = ElasticsearchTool.hit2id(hit)

            return [
                {"update": {"_id": id_this, "_index": index, "_type": "doc"}},
                {"doc": {"v2": v2}},
            ]

        actions = lchain(*map(hit2actions, hits))
        ElasticsearchTool.actions2execute_bulk(client, actions)
