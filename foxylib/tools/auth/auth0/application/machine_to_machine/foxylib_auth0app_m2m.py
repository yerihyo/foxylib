import logging
import os
from dataclasses import dataclass, asdict
from functools import reduce, lru_cache
from typing import Optional
from urllib.parse import urlencode

import requests
from dacite import from_dict

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.auth.auth0.application.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool, Auth0M2MInfo
from foxylib.tools.auth.auth0.foxylib_auth0_api import FoxylibAuth0API
from foxylib.tools.collections.collections_tool import DictTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool
from foxylib.tools.url.url_tool import URLTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 4, FILE_DIR)


class FoxylibAuth0appM2M:
    @classmethod
    def domain(cls):
        return FoxylibEnv.key2value("AUTH0_DOMAIN")

    @classmethod
    def client_id(cls):
        return FoxylibEnv.key2value("AUTH0_M2M_CLIENT_ID")

    @classmethod
    def client_secret(cls):
        return FoxylibEnv.key2value("AUTH0_M2M_CLIENT_SECRET")

    @classmethod
    @lru_cache(maxsize=2)
    def m2m_info(cls) -> Auth0M2MInfo:
        j_info = {
            'api_info':FoxylibAuth0API.api_info(),
            'client_id':cls.client_id(),
            'client_secret':cls.client_secret(),
        }
        m2m_info = from_dict(Auth0M2MInfo, j_info)
        return m2m_info

    @classmethod
    def users(cls):
        logger = FoxylibLogger.func_level2logger(cls.users, logging.DEBUG)

        url = f'{cls.domain()}/api/v2/users'
        token =  cls.m2m_info().token()
        logger.debug({'token':token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(url, headers=headers,)

        j_response = response.json()

        return j_response


@dataclass(frozen=True)
class TicketOption:
    ticket_type: Optional[str] = None
    locale: Optional[str] = None
    website_name: Optional[str] = None

    class TicketType:
        INVITATION = 'invitation'
        PASSWORD_CHANGE = 'password_change'

    class Locale:
        KO = 'ko'
        EN = 'en'

    @classmethod
    def option_str_invitation_ko(cls, website_name=None):
        option = cls(ticket_type=cls.TicketType.INVITATION,
                     locale=cls.Locale.KO,
                     website_name=website_name
                     )
        return urlencode(DictTool.nullvalues2excluded(asdict(option)))

    @classmethod
    def ticket2invitation_ko(cls, ticket, website_name=None):
        return ticket + TicketOption.option_str_invitation_ko(website_name=website_name)

        # option = cls.option_invitation_ko()
        # urlencode(asdict(option))
        # url_out = URLTool.append_query2url(ticket, asdict(option))
        # return url_out


