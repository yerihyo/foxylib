import logging
import random
import string
from dataclasses import dataclass
from functools import lru_cache

from cachetools import TTLCache, cachedmethod

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class Auth0Tool:
    @classmethod
    def generate_password(cls):
        logger = FoxylibLogger.func_level2logger(
            cls.generate_password, logging.DEBUG)

        password = None

        letters = string.digits + string.ascii_letters + string.punctuation
        logger.debug({'letters':letters})
        # raise Exception({'letters':letters})
        length = 12

        def password2is_valid(password_: str):
            if not password_:
                return False

            if password_.isalnum():
                return False

            return True

        while not password2is_valid(password):
            password = ''.join(random.choice(letters) for i in range(length))
            # logger.debug({'password':password})

        return password


@dataclass(frozen=True)
class Auth0APIInfo:
    domain: str
    identifier: str
    # audience: str


@dataclass(frozen=True,)
class Auth0AppInfo:
    api_info: Auth0APIInfo
    client_id: str
    client_secret: str
    # token: Optional[str] = None

    # @classmethod
    @lru_cache(maxsize=1)
    def cache(self):
        return TTLCache(maxsize=1, ttl=36000 - 1000)

    @cachedmethod(lambda c: c.cache())
    def token(self):
        from foxylib.tools.auth.auth0.application.machine_to_machine.auth0_m2m_tool import \
            Auth0M2MTool
        return Auth0M2MTool._info2token(self)
