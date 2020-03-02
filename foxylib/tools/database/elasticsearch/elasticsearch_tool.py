from datetime import datetime

from elasticsearch import NotFoundError
from elasticsearch.helpers import bulk, scan
from nose.tools import assert_equal

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key, lchain, f_vwrite2f_hvwrite
from foxylib.tools.json.json_tool import jdown
# logger = logging.getLogger(__name__)
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class ElasticsearchTool:
    class Type:
        DOCUMENT = 'document'
        _DOC = "_doc"

    # @classmethod
    # @lru_cache(maxsize=2)
    # def env2client(cls, *_, **__):
    #     logger = FoxylibLogger.func2logger(cls.env2client)
    #
    #     auth = os.environ.get("ELASTICSEARCH_AUTH")
    #     host = os.environ.get("ELASTICSEARCH_HOST")
    #     logger.info({"auth":auth, "host":host})
    #
    #     if auth:
    #         return Elasticsearch([auth], *_, **__)
    #
    #     if host:
    #         return Elasticsearch([host], *_, **__)
    #
    #     raise Exception("ELASTICSEARCH_HOST not defined")

    @classmethod
    def index2exists(cls, es_client, es_index):
        return es_client.indices.exists(index=es_index)

    @classmethod
    def index2create_or_skip(cls, es_client, es_index, body=None):
        if cls.index2exists(es_client,es_index):
            return

        j_index = es_client.indices.create(index=es_index, body=body)


        return j_index

    @classmethod
    def ids2delete(cls, es_client, es_index, ids,):
        j = {
            "query": {
                "terms": {
                    "_id": ids,
                }
            }
        }
        return es_client.delete_by_query(es_index, j)

    @classmethod
    def delete_index_if_exsists(cls, es_client, es_index,):
        if not es_client.indices.exists(index=es_index): return

        es_client.indices.delete(index=es_index)

    @classmethod
    def j_result2j_hit_list(cls, j_result):
        j_hit_list = jdown(j_result, ["hits","hits"])
        return j_hit_list

    @classmethod
    def j_result2scroll_id(cls, j_result): return j_result["_scroll_id"]

    @classmethod
    def j_result2total_count(cls, j_result):
        return jdown(j_result, ["hits", "total", "value"])

    @classmethod
    def index2ids(cls, es_client, index):
        if not ESTool.index2exists(es_client, index):
            raise StopIteration()

        j_iter = scan(es_client,
                         query={"query": {"match_all": {}}, "stored_fields": []},
                         index=index,)
        for j in j_iter:
            yield j["_id"]

    @classmethod
    def j_result2j_hit_singleton(cls, j_result):
        j_hits = cls.j_result2j_hit_list(j_result)
        assert_equal(len(j_hits), 1)

        return j_hits[0]

    @classmethod
    def j_result2j_source_singleton(cls, j_result):
        j_hit = cls.j_result2j_hit_singleton(j_result)
        return j_hit["_source"]

    @classmethod
    def j_result2j_hit_src_singleton(cls, j_result):
        return (cls.j_result2j_hit_singleton(j_result),
                cls.j_result2j_source_singleton(j_result),
                )

    @classmethod
    def j_hit2_id(cls, j_hit): return jdown(j_hit, ["_id"])

    @classmethod
    def client_index_query2j_result(cls, es_client, index, j_query):
        logger = FoxylibLogger.func2logger(cls.client_index_query2j_result)
        logger.debug({"index":index, "j_query":j_query})

        j_result = es_client.search(index, j_query)
        return j_result

    @classmethod
    def item_count2request_timeout_default(cls, item_count):
        return item_count*10

    @classmethod
    def search_scroll2result_iter(cls, es_client, search_kwargs, scroll, ):
        logger = FoxylibLogger.func2logger(cls.search_scroll2result_iter)

        j_result = es_client.search(scroll=scroll, **search_kwargs)
        while True:
            j_hit_list = ESTool.j_result2j_hit_list(j_result)
            if not j_hit_list:
                break

            yield j_result

            scroll_id = cls.j_result2scroll_id(j_result)
            j_result = es_client.scroll(scroll_id=scroll_id, scroll=scroll)


    @classmethod
    # https://stackoverflow.com/questions/31635828/python-elasticsearch-client-set-mappings-during-create-index
    def fieldname_list2j_mapping_fielddata(cls, fieldname_list):
        j_property_list = [{fieldname:
                                {"type": "text",
                                 "fielddata": True,
                                 }
                            }
                           for fieldname in fieldname_list]

        j_properties = merge_dicts(j_property_list, vwrite=vwrite_no_duplicate_key, )
        return {"properties": j_properties}

    @classmethod
    def fieldname_list2set_fielddata(cls, es_client, index, fieldname):
        j_mapping = cls.fieldname_list2j_mapping_fielddata(fieldname)
        es_client.indices.put_mapping(index=index, body=j_mapping)


    @classmethod
    def aggrname2j_bucket_list(cls, j_result, aggrname):
        return jdown(j_result, ["aggregations",aggrname,"buckets"])

    @classmethod
    def j_hit2score(cls, j_hit): return j_hit["_score"]




class BulkTool:
    class Field:
        ID = "_id"
        INDEX = "_index"
        SOURCE = "_source"
        TYPE = "_type"
        OP_TYPE = "_op_type"


    @classmethod
    def j_action2id(cls, j): return j.get(cls.Field.ID)
    @classmethod
    def j_action2index(cls, j): return j.get(cls.Field.INDEX)
    @classmethod
    def j_action2body(cls, j): return j.get(cls.Field.SOURCE)
    @classmethod
    def j_action2doc_type(cls, j): return j.get(cls.Field.TYPE)
    @classmethod
    def j_action2op_type(cls, j): return j.get(cls.Field.OP_TYPE, cls.op_type_default())

    @classmethod
    def op_type_default(cls): return "index"

    @classmethod
    def bulk(cls, es_client, j_action_list, run_bulk=True, es_kwargs=None,):
        logger = FoxylibLogger.func2logger(cls.bulk)

        n = len(j_action_list)
        count_list = [n*i//100 for i in range(100)]

        _run_bulk = run_bulk and n>1
        if _run_bulk:
            return bulk(es_client, j_action_list, **es_kwargs)
        else:
            result_list = []
            for i, j_action in enumerate(j_action_list):
                if i in count_list:
                    logger.debug({"i/n":"{}/{}".format(i+1,n),
                                  # "j_action":j_action,
                                  })
                    # raise Exception()

                op_type = cls.j_action2op_type(j_action)

                if op_type == "index":
                    result = cls._j_action2op_index(es_client, j_action, es_kwargs=es_kwargs)
                    result_list.append(result)
                else:
                    raise NotImplementedError()
            return result_list

    @classmethod
    def _j_action2op_index(cls, es_client, j_action, es_kwargs=None):
        id = cls.j_action2id(j_action)
        index = cls.j_action2index(j_action)
        body = cls.j_action2body(j_action)
        doc_type = cls.j_action2doc_type(j_action)
        op_type = cls.j_action2op_type(j_action)
        assert_equal(op_type, "index")

        h = merge_dicts([{"id":id, "index":index, "body":body, "doc_type":doc_type,},
                         es_kwargs], vwrite=vwrite_no_duplicate_key)
        return es_client.index(**h)

class ElasticsearchQuery:
    @classmethod
    def j_all(cls):
        j_query = {
            "query": {
                "match_all": {}
            }
        }
        return j_query

    @classmethod
    def jqi2jq(cls, j): return {"query":j}

    @classmethod
    def j_function_score2jq(cls, j): return {"query": j}

    @classmethod
    def jqi2prefix(cls, jqi): return {"prefix":jqi}
    @classmethod
    def jqi_all(cls): return {"match_all": {}}

    @classmethod
    def id_list2jqi(cls, doc_id_list):
        return {"terms": {"_id": doc_id_list}}

    @classmethod
    def field_values2jqi_terms(cls, field, value_list,):
        return {"terms": {field: value_list}}

    @classmethod
    def boost2jqi_terms(cls, boost):
        return {"terms": {"boost":boost}}

    @classmethod
    def field_values_boost2jqi_terms(cls, field, value_list, boost):
        l = [cls.field_values2jqi_terms(field, value_list),
             cls.boost2jqi_terms(boost),
             ]
        return merge_dicts(l, vwrite=f_vwrite2f_hvwrite(vwrite_no_duplicate_key))


    @classmethod
    def jqi2boosted(cls, jqi, boost):
        return {"function_score": merge_dicts([cls.jqi2jq(jqi), {"boost":boost}])}

    @classmethod
    def jq_from(cls, start):
        return {"from": start, }

    @classmethod
    def jq_size(cls, size):
        return {"size": size,}

    @classmethod
    def jq_track_total_hits(cls, track_total_hits=True,):
        return {"track_total_hits": track_total_hits,}

    @classmethod
    def fieldname_list2j_includes(cls, fieldname_list):
        return {"includes": fieldname_list}

    @classmethod
    def field_list2jq__source(cls, l):
        return {"_source": l,}


    @classmethod
    def j_query_list2j_match(cls, j_match_list):
        return {
            "match": j_match_list
        }

    @classmethod
    def kv2jqi_term(cls, k, v): return {"term": {k: v}}
    @classmethod
    def kl2jqi_terms(cls, k, l): return {"terms": {k: l}}

    @classmethod
    def kl2jqi_match(cls, k, l): return {"match": {k: l}}

    @classmethod
    def jqi_list2must(cls, l):
        if len(l)==1: return l[0]
        return {"bool": {"must": l}}

    @classmethod
    def jqi_list2must_not(cls, l):
        return {"bool": {"must_not": l}}

    @classmethod
    def jqi_list_pair2must_mustnot(cls, jqi_list_must, jqi_list_must_not):
        l = [cls.jqi_list2must(jqi_list_must),
             cls.jqi_list2must_not(jqi_list_must_not),
             ]
        return merge_dicts(l, vwrite=f_vwrite2f_hvwrite(vwrite_no_duplicate_key))

    @classmethod
    def jqi_list2should(cls, l):
        return {"bool": {"should": l}}

    @classmethod
    def jq_functions2j_function_score(cls, jq, function_list, options):
        h = merge_dicts([jq,
                         {"functions": function_list},
                         options,
                         ])
        return {"function_score":h}


    @classmethod
    def query_fields2jqi_multimatch(cls, str_query, field_list):
        return {
            "multi_match": {
                "query": str_query,
                "fields": field_list
            }
        }

    @classmethod
    def l2jq_sort(cls, l): return {"sort":l}

    @classmethod
    def index_jq_list2j_msearch(cls, index_jq_list):
        j_msearch = lchain(*[[{'index': index}, jq, ]
                             for index, jq in index_jq_list])
        return j_msearch

    @classmethod
    def fieldname2aggrname_default(cls, fieldname):
        return "-".join(["groupby",fieldname])

    @classmethod
    def aggrname_fieldname2jq_agg_groupby(cls, aggrname, fieldname,):
        jqi_term = ESQuery.kl2jqi_terms("field", fieldname)

        return {"aggs": {aggrname: jqi_term}}

# class ElasticsearchQueryItem:
#     @classmethod
#     def field_j_field2jqi_match(cls, field, jqif):
#         return {"match": {field: jqif}}
#
#     @classmethod
#     def field_j_field2jqi_match_phrase(cls, field, jqif):
#         return {"match_phrase": {field: jqif}}
#
#
# class ElasticsearchQueryItemField:
#     @classmethod
#     def jqif_op_and(cls,):
#         return {"operator": "and"}
#
#     @classmethod
#     def jqif_op_or(cls,):
#         return {"operator": "or"}
#
#     @classmethod
#     def query2jqif_query(cls, query):
#         return {"query": query}
#
#     @classmethod
#     def boost2jqif_boost(cls, boost):
#         return {"boost": boost}


class ElasticsearchFunction:
    class Decay:
        class Function:
            LINEAR = "linear"
        Func = Function

    @classmethod
    def jf_decay(cls, decay_function, fieldname, origin, scale, offset=None, decay=None):
        l = [{"origin": origin},
             {"scale": scale},
             ]
        if offset is not None: l.append({"offset": offset})
        if decay is not None: l.append({"decay": decay})

        j = {
            decay_function: {
                fieldname: merge_dicts(l)
            }
        }
        return j

    """
    Document of exact date : score of 'multiplier' added
    Document of past 'dates_full_decay' : no score added
    """
    @classmethod
    def linear_timedelta_decay(cls, fieldname, dates_full_decay, max_value):
        # multiplier = dates_full_decay / 365 * decay_per_year
        multiplier = max_value

        dt_now = datetime.now()
        scale = "{}d".format(dates_full_decay//2)
        jf_decay = cls.jf_decay(cls.Decay.Func.LINEAR, fieldname, dt_now.date().isoformat(), scale=scale, decay=0.5)

        jf = merge_dicts([{"weight":multiplier}, jf_decay])
        return jf

class IndexTool:
    @classmethod
    def client_name2exists(cls, es_client, index):
        return es_client.indices.exists(index=index)

    @classmethod
    def client_name2gorc(cls, es_client, name):
        j_index = es_client.indices.get(name)
        if j_index:
            return j_index

        j_index = es_client.indices.create(name)
        return j_index

    @classmethod
    def delete(cls, es_client, index):
        j_result = es_client.indices.delete(index)
        return j_result


class IndexAliasTool:
    @classmethod
    def delete(cls, es_client, alias):
        logger = FoxylibLogger.func2logger(cls.create)
        index_list = cls.alias2indexes(es_client, alias)
        if index_list is None: return

        return es_client.indices.delete_alias(index=",".join(index_list), name=alias)

    @classmethod
    def create(cls, es_client, index, alias):
        logger = FoxylibLogger.func2logger(cls.create)
        logger.debug({"index":index, "alias":alias})

        j_result = es_client.indices.put_alias(index, alias)
        return j_result

    @classmethod
    def create_or_update(cls, es_client, alias, index):
        # GET / dev - precedents / _alias / *
        cls.delete(es_client, alias)
        return cls.create(es_client, index, alias)

    @classmethod
    def alias2indexes(cls, es_client, alias):
        logger = FoxylibLogger.func2logger(cls.alias2indexes)

        try:
            j_result = es_client.indices.get_alias(name=alias)
        except NotFoundError:
            return None

        index_list = list(j_result.keys())
        return index_list



ESTool = ElasticsearchTool
ESQuery = ElasticsearchQuery
j_result2j_hit_list = ElasticsearchTool.j_result2j_hit_list
