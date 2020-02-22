import logging
import os
import sys

import yaml
from future.utils import lmap, lfilter

from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import BooleanTool
from foxylib.tools.string.string_tool import str2strip


class EnvTool:
    class K:
        ENV = "ENV"


    @classmethod
    def kv_list2str_export(cls, kv_list):
        str_export = "\n".join(['export {0}="{1}"'.format(k, v_yaml) for k, v_yaml in kv_list])
        return str_export

    @classmethod
    def yaml_str2kv_list(cls, tmplt_str, envname_list):
        logger = FoxylibLogger.func2logger(cls.yaml_str2kv_list)

        #s = Jinja2Tool.tmplt_file2str(tmplt_filepath, data)
        j = yaml.load(tmplt_str)

        l = []
        for k, v in j.items():
            if not isinstance(v,dict):
                l.append( (k,v) )
                continue

            vv = DictTool.keys2v_first_or_default(v, envname_list)
            if vv is None: continue

            l.append((k,vv))

        logger.info({"l": l,
                     "tmplt_str": tmplt_str,
                     })

        return l

    @classmethod
    def k2v(cls, key, default=None):
        return os.environ.get(key, default)

    @classmethod
    def k_list2v(cls, key_list, default=None):
        for key in key_list:
            if key not in os.environ:
                continue

            return os.environ[key]

        return default


    @classmethod
    def key2nullboolean(cls, key):
        v = cls.k2v(key)
        nb = BooleanTool.parse2nullboolean(v)
        return nb

    @classmethod
    def key2is_true(cls, key):
        nb = cls.key2nullboolean(key)
        return nb is True

    @classmethod
    def key2is_not_true(cls, key):
        return not cls.key2is_true(key)



