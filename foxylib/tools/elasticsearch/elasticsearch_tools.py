import logging
import os
from functools import lru_cache

from elasticsearch import Elasticsearch


logger = logging.getLogger(__name__)

class ElasticsearchToolkit:
    @classmethod
    def env2host(cls):
        return os.environ.get("ELASTICSEARCH_HOST")

    @classmethod
    def env2auth(cls):
        return os.environ.get("ELASTICSEARCH_AUTH")

    @classmethod
    @lru_cache(maxsize=2)
    def env2client(cls):
        auth = cls.env2auth()
        host = cls.env2host()
        logger.info({"auth":auth, "host":host})

        if auth:
            return Elasticsearch([auth])

        if host:
            return Elasticsearch([host])

        raise Exception("ELASTICSEARCH_HOST not defined")

    @classmethod
    def product_reference_index(cls):
        return "product-reference-alias"

    # @classmethod
    # def client_index2all(cls, es_client, index,):
    #     return es_client.search(index=index, body={'query': {'match_all': {}}})

ESToolkit = ElasticsearchToolkit
