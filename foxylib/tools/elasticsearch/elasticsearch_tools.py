import logging
import os
from functools import lru_cache

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from nose.tools import assert_equal

from foxylib.tools.json.json_tools import JToolkit, jdown

# logger = logging.getLogger(__name__)
from foxylib.tools.log.logger_tools import FoxylibLogger


class ElasticsearchToolkit:
    @classmethod
    def env2host(cls):
        return os.environ.get("ELASTICSEARCH_HOST")

    @classmethod
    def env2auth(cls):
        return os.environ.get("ELASTICSEARCH_AUTH")

    @classmethod
    @lru_cache(maxsize=2)
    def env2client(cls, *_, **__):
        logger = FoxylibLogger.func2logger(cls.env2client)

        auth = cls.env2auth()
        host = cls.env2host()
        logger.info({"auth":auth, "host":host})

        if auth:
            return Elasticsearch([auth], *_, **__)

        if host:
            return Elasticsearch([host], *_, **__)

        raise Exception("ELASTICSEARCH_HOST not defined")

    @classmethod
    def index2create_or_skip(cls, es_client, es_index, body=None):
        if es_client.indices.exists(index=es_index):
            return

        j_index = es_client.indices.create(index=es_index, body=body)


        return j_index

    @classmethod
    def index2delete_or_skip(cls, es_client, es_index,):
        if not es_client.indices.exists(index=es_index): return

        es_client.indices.delete(index=es_index)

    @classmethod
    def j_result2j_hit_list(cls, j_in):
        j_out = jdown(j_in, ["hits","hits"])
        return j_out

    @classmethod
    def index2ids(cls, es_client, index):
        for j in scan(es_client,
                         query={"query": {"match_all": {}}, "store_fields": []},
                         index=index,):
            yield j["_id"]



class BulkToolkit:
    @classmethod
    def j_action2id(cls, j): return j.get("_id")
    @classmethod
    def j_action2index(cls, j): return j.get("_index")
    @classmethod
    def j_action2body(cls, j): return j.get("_source")
    @classmethod
    def j_action2doc_type(cls, j): return j.get("_type")
    @classmethod
    def j_action2op_type(cls, j): return j.get("_op_type", cls.op_type_default())

    @classmethod
    def op_type_default(cls): return "index"

    @classmethod
    def bulk(cls, es_client, j_action_list, run_bulk=True,):
        logger = FoxylibLogger.func2logger(cls.bulk)

        n = len(j_action_list)
        count_list = [n*i//100 for i in range(100)]

        _run_bulk = run_bulk and n>1
        if _run_bulk:
            return bulk(es_client, j_action_list)
        else:
            for i, j_action in enumerate(j_action_list):
                if i in count_list:
                    logger.debug({"i/n":"{}/{}".format(i+1,n),
                                  "j_action":j_action,
                                  })

                op_type = cls.j_action2op_type(j_action)

                if op_type == "index":
                    cls._j_action2index(es_client, j_action)
                else:
                    raise NotImplementedError()

    @classmethod
    def _j_action2index(cls, es_client, j_action):
        id = cls.j_action2id(j_action)
        index = cls.j_action2index(j_action)
        body = cls.j_action2body(j_action)
        doc_type = cls.j_action2doc_type(j_action)
        op_type = cls.j_action2op_type(j_action)
        assert_equal(op_type, "index")

        h = {"id":id, "index":index, "body":body, "doc_type":doc_type,}
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
    def j_size(cls, size):
        return {"size": size,}

    @classmethod
    def j_track_total_hits(cls, track_total_hits=True,):
        return { "track_total_hits": track_total_hits,}

    @classmethod
    def fieldname_list2j_source(cls, fieldname_list):
        return {"includes": fieldname_list}

    @classmethod
    def str_field2j_source(cls, str_field):
        return {"_source": str_field,}


    @classmethod
    def j_query_list2j_must(cls, j_query_list):
        return {
            "bool": {
                "must": j_query_list
            }
        }

class IndexToolkit:
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

ESToolkit = ElasticsearchToolkit
ESQuery = ElasticsearchQuery
