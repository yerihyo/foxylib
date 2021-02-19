import json
import logging
from dataclasses import dataclass
from functools import lru_cache
from pprint import pformat

import requests
from cachetools import TTLCache, cached, cachedmethod

from foxylib.tools.auth.auth0.auth0_tool import Auth0APIInfo
from foxylib.tools.collections.collections_tool import l_singleton2obj, DictTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool
from foxylib.tools.url.url_tool import URLTool


@dataclass(frozen=True,)
class Auth0M2MInfo:
    api_info: Auth0APIInfo
    client_id: str
    client_secret: str
    # token: Optional[str] = None

    # @classmethod
    @lru_cache(maxsize=2)
    def cache(self):
        return TTLCache(maxsize=2, ttl=36000 - 1000)

    @cachedmethod(lambda c: c.cache())
    def token(self):
        return Auth0M2MTool._info2token(self)


class Auth0M2MTool:

    @classmethod
    def _info2token(cls, m2m_info: Auth0M2MInfo):
        logger = FoxylibLogger.func_level2logger(
            cls._info2token, logging.DEBUG)

        domain = m2m_info.api_info.domain
        payload = {'client_id': m2m_info.client_id,
                   'client_secret': m2m_info.client_secret,
                   'audience': m2m_info.api_info.identifier,
                   'grant_type': 'client_credentials',
                   }
        url = f'{domain}/oauth/token'
        response = requests.post(url, json=payload)

        logger.debug(pformat({
            'payload': payload,
            'response':response,
        }))

        j_body = response.json()
        return j_body['access_token']

    @classmethod
    def email_connection2user(cls, m2m_info: Auth0M2MInfo, email, connection):
        logger = FoxylibLogger.func_level2logger(cls.email_connection2user,
                                                 logging.DEBUG)

        q = " AND " .join([
            f'identities.connection:"{connection}"',
            f'email:"{email}"',
            ])

        logger.debug(pformat({'q': q}))
        users = cls.users(m2m_info, payload={'q': q})

        logger.debug(pformat({'users':users}))
        user = l_singleton2obj(users, allow_empty_list=True)
        return user

    @classmethod
    def users(cls, m2m_info: Auth0M2MInfo, payload=None):
        logger = FoxylibLogger.func_level2logger(cls.users,
                                                 logging.DEBUG)

        identifier = m2m_info.api_info.identifier
        token = m2m_info.token()

        endpoint = f'{identifier}users'

        # logger.debug(pformat({'payload': payload}))

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(endpoint, headers=headers, params=payload)
        users = response.json()

        logger.debug(pformat({
            'users': users,
            'response.url': response.url,
            'response': response, }))

        if response.status_code != 200:
            return None

        return users

    @classmethod
    def delete_user(cls, m2m_info: Auth0M2MInfo, user_id):
        logger = FoxylibLogger.func_level2logger(cls.delete_user,
                                                 logging.DEBUG)

        identifier = m2m_info.api_info.identifier
        token = m2m_info.token()
        endpoint = f'{identifier}users/{user_id}'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.delete(endpoint, headers=headers,)
        return response.ok

    @classmethod
    def create_user(cls, m2m_info: Auth0M2MInfo, body,):
        logger = FoxylibLogger.func_level2logger(
            cls.create_user, logging.DEBUG)

        identifier = m2m_info.api_info.identifier
        token = m2m_info.token()
        endpoint = f'{identifier}users'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.post(endpoint, headers=headers, json=body)
        j_user = response.json()

        logger.debug(pformat({
            'endpoint': endpoint, 'token': token, 'body': body,
            'j_user': j_user, 'response': response, }))

        if not response.ok:
            return None

        return j_user

    @classmethod
    def change_password(cls, m2m_info: Auth0M2MInfo, email):

        domain = m2m_info.api_info.domain
        payload = {"client_id": m2m_info.client_id,
                   "email": email,
                   "connection": Auth0Connection.username_password_auth(),
                   }

        endpoint = f'{domain}/dbconnections/change_password'
        response = requests.post(endpoint, json=payload)

        if not response.ok:
            return None

        return response.json()

    @classmethod
    def create_password_change_ticket(
            cls, m2m_info: Auth0M2MInfo, user_id, result_url=None):
        """
        reference: https://auth0.com/docs/auth0-email-services/send-email-invitations-for-application-signup
        """
        logger = FoxylibLogger.func_level2logger(
            cls.create_password_change_ticket, logging.DEBUG)

        identifier = m2m_info.api_info.identifier
        token = m2m_info.token()

        headers = RequestsTool.token2header_bearer(token)

        body = DictTool.nullvalues2excluded({
            "result_url": result_url,
            "user_id": user_id,
            "ttl_sec": 60 * 60 * 2,  # 2 hours
            "mark_email_as_verified": True,
            # "includeEmailInRedirect": False,
            "client_id": m2m_info.client_id,
        })
        url = f'{identifier}tickets/password-change'
        response = requests.post(url, headers=headers, json=body)
        # logger.debug({
        #     'json.dumps(body)': json.dumps(body),
        # })
        logger.debug(pformat({
            'body': body,
            'response': response,
            'response.json()': response.json(),
        }))

        if not response.ok:
            return None

        j_response = response.json()
        ticket = j_response['ticket']

        return ticket


class Auth0Connection:
    @classmethod
    def username_password_auth(cls):
        return "Username-Password-Authentication"


class Auth0User:
    @classmethod
    def user2user_id(cls, user):
        return user['user_id']



