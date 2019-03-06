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

        env = os.environ.get(cls.Key.ENV)
        for k,h in j.items():

            v = DictToolkit.keys2v_first_or_default(h, [env, cls.EnvName.DEFAULT])
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
    def k2v(cls, j, key, envname=None, default=None,):
        if not j: return default
        if key not in j: return default

        v = j[key]
        if not isinstance(v,dict): return v

        envkey_list = [envname, cls.Key._DEFAULT_]
        for ek in envkey_list:
            if not ek: continue
            if ek not in v: continue
            return v[ek]

        if cls.Key._DEFAULT_ in v: return v[cls.Key._DEFAULT_]

        return default

    @classmethod
    def k2v_env_or_yaml(cls, j, key, envname=None, default=None,):
        if key in os.environ:
            return os.environ[key]

        return cls.k2v(j, key, envname=envname, default=default)
