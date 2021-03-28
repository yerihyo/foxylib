import json

from bson.json_util import dumps
from future.utils import lmap

from foxylib.tools.collections.iter_tool import IterTool


class BsonTool:
    @classmethod
    def is_btag(cls, str_in):
        return str_in.startswith("$")

    @classmethod
    def bson2json(cls, b_in):
        def json2btag_cleaned(j_in):
            if isinstance(j_in, list):
                return lmap(json2btag_cleaned, j_in)

            if isinstance(j_in, dict):
                has_bson_tag = any(filter(cls.is_btag, j_in.keys()))
                if not has_bson_tag:
                    return {k: json2btag_cleaned(v)
                            for k, v in j_in.items()}

                assert (len(j_in), 1)
                v = IterTool.iter2singleton(j_in.values())
                return json2btag_cleaned(v)

            return j_in

        b_str = dumps(b_in)
        j_tmp = json.loads(b_str)
        return json2btag_cleaned(j_tmp)
