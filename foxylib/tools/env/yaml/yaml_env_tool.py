import logging
import os
import re
from functools import lru_cache
from pathlib import Path
from pprint import pprint

import yaml
from future.utils import lfilter
from jinja2 import Environment, StrictUndefined

from foxylib.tools.collections.collections_tool import merge_dicts
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.jinja2.jinja2_tool import Jinja2Renderer
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import str2strip


class Lpassline:
    @classmethod
    @lru_cache(maxsize=2)
    def pattern_comment(cls):
        return re.compile(r"^\s*[#;]")

    @classmethod
    def lpassline_context2filepath(cls, lpassline, h_context):
        logger = FoxylibLogger.func_level2logger(cls.lpassline_context2filepath, logging.DEBUG)

        def lpassline2filepath_prejinja(lpassline_):
            if not lpassline_:
                return None

            str_strip = str2strip(lpassline_)
            logger.debug({"str_strip": str_strip})
            if not str_strip:
                return None

            m = cls.pattern_comment().match(str_strip)
            if m:
                return None

            return lpassline_.split(maxsplit=1)[1]

        filepath_prejinja = lpassline2filepath_prejinja(lpassline)
        if not filepath_prejinja:
            return None

        filepath = Jinja2Renderer.text2text(filepath_prejinja, data=h_context)
        return filepath


class YamlEnvFile:
    class EnvKey:
        DEFAULT = "__DEFAULT__"

    @classmethod
    def filepath2is_yaml(cls, filepath):
        if not filepath:
            return False

        if filepath.endswith('.yml'):
            return True

        if filepath.endswith('.yaml'):
            return True

        return False

    @classmethod
    def filepath_context2kv_list(cls, filepath, h_context):
        logger = FoxylibLogger.func_level2logger(cls.filepath_context2kv_list, logging.DEBUG)
        logger.debug({'filepath': filepath})
        if not YamlEnvFile.filepath2is_yaml(filepath):
            return []

        envname_list = lfilter(bool, [h_context.get("ENV"), cls.EnvKey.DEFAULT])

        jinja2_env = Environment(undefined=StrictUndefined)
        str_yaml = Jinja2Renderer.textfile2text(filepath, data=h_context, env=jinja2_env)

        j_yaml = yaml.load(str_yaml, Loader=yaml.SafeLoader)
        kv_list = EnvTool.yaml_envnames2kv_list(j_yaml, h_context, envname_list)
        return kv_list

    @classmethod
    def filepath_context2envvar_list(cls, filepath, h_context):
        logger = FoxylibLogger.func_level2logger(cls.filepath_context2envvar_list, logging.DEBUG)

        kv_list = cls.filepath_context2kv_list(filepath, h_context)
        # logger.debug({"kv_list": kv_list})
        return [f'{k}="{v}"' for k, v in kv_list]

    # @classmethod
    # def lpassline_context2kv_list(cls, lpassline, h_context):
    #     logger = FoxylibLogger.func_level2logger(cls.lpassline_context2kv_list, logging.DEBUG)
    #
    #     yaml_filepath = Lpassline.lpassline_context2filepath(lpassline, h_context)
    #     if not yaml_filepath:
    #         return []
    #
    #     kv_list = cls.filepath_context2kv_list(yaml_filepath, h_context)
    #     return kv_list
