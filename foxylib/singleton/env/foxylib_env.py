import logging
import os
from functools import lru_cache, reduce
from pathlib import Path

import yaml
from yaml import BaseLoader

from foxylib.singleton.jinja2.foxylib_jinja2 import FoxylibJinja2
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.native_tool import BooleanTool
from foxylib.tools.string.string_tool import str2lower

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)


class FoxylibEnv:
    class Value:
        LOCAL = "local"
        DEV = "dev"
        STAGING = "staging"
        PROD = "prod"

        @classmethod
        def list(cls):
            return [cls.LOCAL, cls.DEV, cls.PROD]

    @classmethod
    def env(cls):
        logger = FoxylibLogger.func_level2logger(cls.env, logging.DEBUG)

        env_raw = EnvTool.env_raw()
        # logger.debug({"env_raw":env_raw})
        return cls.env2norm(env_raw) or "local"

    @classmethod
    def env2norm(cls, env):
        _env = str2lower(env)

        if _env in {"prod", "production", }:
            return cls.Value.PROD

        if _env in {"staging", }:
            return cls.Value.STAGING

        if _env in {"dev", "develop", "development", }:
            return cls.Value.DEV

        if _env in {"local", }:
            return cls.Value.LOCAL

        return _env

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def _json_yaml(cls,):
        logger = FoxylibLogger.func_level2logger(cls._json_yaml, logging.DEBUG)

        filepath = os.path.join(REPO_DIR, "env", "yaml", "env.part.yaml")
        logger.debug({"filepath":filepath,
                      "os.path.exists(filepath)":os.path.exists(filepath),
                      })

        if not os.path.exists(filepath):
            return None

        data = {"HOME": str(Path.home()),
                "REPO_DIR": REPO_DIR,
                }
        utf8 = FoxylibJinja2.textfile2text(filepath, data)
        json_yaml = yaml.load(utf8, Loader=BaseLoader)
        return json_yaml

    @classmethod
    def _env2target_envs(cls, env):
        __DEFAULT__ = "__DEFAULT__"
        env_norm = cls.env2norm(env)

        if env_norm in {cls.Value.DEV, cls.Value.STAGING, cls.Value.PROD}:
            return [env, __DEFAULT__]

        if env_norm in {cls.Value.LOCAL}:
            return [env, cls.Value.DEV, __DEFAULT__]

        raise NotImplementedError({"env": env})

    @classmethod
    def env_key2value(cls, env, k):
        logger = FoxylibLogger.func_level2logger(cls.env_key2value, logging.DEBUG)
        # return os.environ.get(k)

        json_yaml = cls._json_yaml()
        # logger.debug({"json_yaml":json_yaml})

        envs = cls._env2target_envs(env)

        return EnvTool.context_json_envs_key2value(os.environ, json_yaml, envs, k)

    @classmethod
    def env2dict(cls, env):
        return {key: cls.env_key2value(env, key) for key in cls.keys()}

    @classmethod
    def keys(cls):
        return list(cls._json_yaml().keys())

    @classmethod
    def key2value(cls, key):
        return cls.env_key2value(cls.env(), key)

    @classmethod
    def key2nullboolean(cls, key):
        v = cls.key2value(key)
        nb = BooleanTool.parse2nullboolean(v)
        return nb


