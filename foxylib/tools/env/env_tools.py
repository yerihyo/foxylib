import os

from future.utils import lfilter

from foxylib.tools.collections.collections_tools import DictToolkit
from foxylib.tools.json.yaml_tools import YAMLToolkit
from foxylib.tools.native.builtin_tools import BooleanToolkit


class EnvToolkit:
    class Key:
        ENV = "ENV"

    class EnvName:
        DEFAULT = "default"
        DEV = "dev"
        PRODUCTION = "production"
        STAGING = "staging"


    @classmethod
    def yaml_filepath2env(cls, filepath):
        j = YAMLToolkit.filepath2j(filepath)

        env = os.environ.get(cls.K.ENV)
        for k,h in j.items():

            v = DictToolkit.keys2v_first_or_none(h, [env, cls.Env.DEFAULT])
            if v is None: continue

            os.environ[k] = v
        return os.environ

    @classmethod
    def k2v(cls, key): return os.environ[key]

    @classmethod
    def k2v_or_default(cls, key, default=None):
        return os.environ.get(key, default)
    key2value = k2v

    @classmethod
    def key2nullboolean(cls, key):
        v = cls.k2v(key)
        nb = BooleanToolkit.parse2nullboolean(v)
        return nb

    @classmethod
    def key2is_true(cls, key):
        nb = cls.key2nullboolean(key)
        return nb is True

    @classmethod
    def key2is_not_true(cls, key):
        return not cls.key2is_true(key)


class YamlConfigToolkit:
    class Key:
        _DEFAULT_ = "_DEFAULT_"

    @classmethod
    def k2v_or_die(cls, j, key, envname=None,):
        v = j[key]
        if not isinstance(v,dict): return v

        if envname and (envname in v):
            return envname[v]

        return v[cls.Key._DEFAULT_]


    @classmethod
    def k2v_or_default(cls, j, key, envname=None, default=None,):
        try:
            return cls.k2v_or_die(j,key,envname=envname,)
        except KeyError:
            return default
