import logging
import os
from dataclasses import dataclass, asdict
from functools import reduce, lru_cache
from typing import Optional
from urllib.parse import urlencode

import requests
from dacite import from_dict
from nose.tools import assert_is_not_none, assert_equal

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.auth.auth0.application.machine_to_machine.auth0_m2m_tool import \
    Auth0M2MTool
from foxylib.tools.auth.auth0.auth0_tool import Auth0AppInfo
from foxylib.tools.auth.auth0.foxylib_auth0_api import FoxylibAuth0API
from foxylib.tools.collections.collections_tool import DictTool, \
    vwrite_overwrite
from foxylib.tools.dataclass.dataclass_tool import DataclassTool
from foxylib.tools.locale.locale_tool import LocaleTool
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
    def app_info(cls) -> Auth0AppInfo:
        j_info = {
            'api_info':FoxylibAuth0API.api_info(),
            'client_id':cls.client_id(),
            'client_secret':cls.client_secret(),
        }
        app_info = from_dict(Auth0AppInfo, j_info)
        return app_info

    @classmethod
    def users(cls):
        logger = FoxylibLogger.func_level2logger(cls.users, logging.DEBUG)

        url = f'{cls.domain()}/api/v2/users'
        token =  cls.app_info().token()
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
    result_url: Optional[str] = None

    class TicketType:
        INVITATION = 'invitation'
        PASSWORD_CHANGE = 'password_change'

    class Locale:
        KO = 'ko'
        EN = 'en'

    @classmethod
    def option2str_invitation(cls, option_in):
        def option2norm(option_):
            if not option_:
                return {}

            if not option_.locale:
                return option_

            lang = LocaleTool.locale2lang(option_.locale)
            option_out = DataclassTool.merge([
                option_in,
                cls(locale=lang),
            ], vwrite=DictTool.VWrite.overwrite)
            return option_out

        j_norm = DictTool.keys2excluded(
            asdict(option2norm(option_in)),
            [DataclassTool.fieldname2checked(cls, 'result_url')],
        )
        return urlencode(DictTool.nullvalues2excluded(j_norm))

    @classmethod
    def ticket2invitation(cls, ticket, option=None):
        assert_is_not_none(ticket)

        if option and option.ticket_type:
            assert_equal(option.ticket_type, cls.TicketType.INVITATION)

        option_out = DataclassTool.merge([
            option if option else None,
            cls(ticket_type=cls.TicketType.INVITATION),
        ], vwrite=DictTool.VWrite.overwrite, )

        invitation = ticket + cls.option2str_invitation(option_out)
        return invitation

    @classmethod
    def user_id2url_invitation(cls, app_info, user_id, option=None):
        logger = FoxylibLogger.func_level2logger(
            cls.user_id2url_invitation, logging.DEBUG)

        ticket_pw_change = Auth0M2MTool.user_id2ticket_password_change(
            app_info, user_id, result_url=option.result_url)

        ticket_invitation = TicketOption.ticket2invitation(
            ticket_pw_change, option=option)

        logger.debug({'ticket_invitation':ticket_invitation})

        return ticket_invitation

