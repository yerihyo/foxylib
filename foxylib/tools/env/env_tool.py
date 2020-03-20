import os
from functools import partial

from future.utils import lmap, lfilter

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class EnvTool:
    # class K:
    #     ENV = "ENV"

    @classmethod
    def env_raw(cls):
        _ENV = os.environ.get("ENV")
        if _ENV:
            return _ENV

        _env = os.environ.get("env")
        if _env:
            return _env

        return None

    # @classmethod
    # def kv_list2str_export(cls, kv_list):
    #     str_export = "\n".join(['export {0}="{1}"'.format(k, v_yaml) for k, v_yaml in kv_list])
    #     return str_export

    # @classmethod
    # def yaml_str2kv_list(cls, tmplt_str, envname_list):
    #     logger = FoxylibLogger.func2logger(cls.yaml_str2kv_list)
    #
    #     #s = Jinja2Tool.tmplt_file2str(tmplt_filepath, data)
    #     j = yaml.load(tmplt_str)
    #
    #     l = []
    #     for k, v in j.items():
    #         if not isinstance(v,dict):
    #             l.append( (k,v) )
    #             continue
    #
    #         vv = DictTool.keys2v_first_or_default(v, envname_list)
    #         if vv is None: continue
    #
    #         l.append((k,vv))
    #
    #     logger.info({"l": l,
    #                  "tmplt_str": tmplt_str,
    #                  })
    #
    #     return l

    @classmethod
    def json_envs_key2value(cls, json_yaml, envs, k):
        if not json_yaml:
            return None
        
        v_raw = json_yaml.get(k)

        if not v_raw:
            return None

        if not isinstance(v_raw, dict):
            return v_raw

        h_child = v_raw

        for env in envs:
            v = h_child.get(env)
            if v is not None:
                return v

        return None

    @classmethod
    def yaml_envnames2kv_list(cls, json_yaml, envs):
        logger = FoxylibLogger.func2logger(cls.yaml_envnames2kv_list)

        key_list = list(json_yaml.keys())
        value_list = lmap(partial(cls.json_envs_key2value, json_yaml, envs), key_list)
        m = len(key_list)

        index_list_valid = lfilter(lambda i:value_list[i] is not None, range(m))
        return lmap(lambda i: (key_list[i], value_list[i]), index_list_valid)






