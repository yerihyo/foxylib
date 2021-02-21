from functools import lru_cache

from dacite import from_dict

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.auth.auth0.auth0_tool import Auth0APIInfo


class FoxylibAuth0API:
    @classmethod
    def domain(cls):
        return FoxylibEnv.key2value("AUTH0_DOMAIN")

    @classmethod
    def identifier(cls):
        return FoxylibEnv.key2value("AUTH0_IDENTIFIER")

    # @classmethod
    # def audience(cls):
    #     return cls.identifier()

    @classmethod
    @lru_cache(maxsize=2)
    def api_info(cls):
        j_info = {'domain': cls.domain(),
                  'identifier': cls.identifier(),
                  # 'audience': cls.audience(),
                  }
        api_info = from_dict(Auth0APIInfo, j_info)
        return api_info
