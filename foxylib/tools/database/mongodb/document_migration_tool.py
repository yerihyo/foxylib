from future.utils import lmap

from foxylib.tools.collections.chunk_tool import ChunkTool
from foxylib.tools.collections.collections_tool import f_iter2f_list
from foxylib.tools.database.mongodb.mongodb_tool import DocumentTool, MongoDBTool
from foxylib.tools.json.json_tool import jdown


class DocumentMigrationTool:
    class Config:
        SELF_REF_CONFIG = "self_ref_config"

    @classmethod
    def j_config2self_ref_config(cls, j_config):
        return jdown(j_config, [cls.Config.SELF_REF_CONFIG])

    @classmethod
    def j_doc_list2self_ref_fixed(cls, j_doc_list, j_config=None):
        self_ref_config = cls.j_config2self_ref_config(j_config)
        if not self_ref_config:
            return j_doc_list

    @classmethod
    def doc_list2migrated(cls, doc_list_in, collection_to, j_config=None, **__):
        j_doc_list_in = lmap(DocumentTool.doc2meta_keys_removed, doc_list_in)
        result = collection_to.insert_many(j_doc_list_in, **__)
        j_doc_list_out_raw = list(MongoDBTool.result2j_doc_iter(result))

        self_ref_config = cls.j_config2self_ref_config(j_config)
        if not self_ref_config:
            return j_doc_list_out_raw


        return result

    @classmethod
    @f_iter2f_list
    def doc_id_list2migrated(cls, doc_id_list, collection_fromto, chunk_size=None, j_config=None,):
        c_from, c_to = collection_fromto

        doc_iter = c_from.find({"_id":{"$in":doc_id_list}})
        for doc_sublist in ChunkTool.chunk_size2chunks(doc_iter, chunk_size=chunk_size):
            yield cls.doc_list2migrated(doc_sublist, c_to, j_config=j_config)

