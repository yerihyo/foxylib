from contextlib import contextmanager
from functools import lru_cache

import cloudinary

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.function.function_tool import FunctionTool


class CloudinaryTool:
    @classmethod
    def url2config(cls, url):
        config = cloudinary.Config()
        parsed_url = config._parse_cloudinary_url(url)
        config._setup_from_parsed_url(parsed_url)
        return config

    @classmethod
    @contextmanager
    def config2activated(cls, config):
        config_prev = cloudinary._config
        try:
            cloudinary._config = config
            yield cloudinary._config
        finally:
            cloudinary._config = config_prev


class FoxylibCloudinary:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def config(cls):
        url = FoxylibEnv.key2value("CLOUDINARY_URL")
        return CloudinaryTool.url2config(url)






