import logging
from dataclasses import dataclass
from pprint import pformat

import logging
from pprint import pformat
from typing import Tuple, List

import requests
from dacite import from_dict

from foxylib.tools.auth.auth0.auth0_tool import Auth0AppInfo
from foxylib.tools.collections.collections_tool import l_singleton2obj, DictTool
from foxylib.tools.database.crud_tool import CRUDResult
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool, \
    FailedRequest

@dataclass
class Auth0User:
    user_id: str
    email_verified: bool
    email: str

    @classmethod
    def user2user_id(cls, user):
        return user['user_id']

    @classmethod
    def user2email_verified(cls, user):
        return user['user_id']


class Auth0M2MTool:

    @classmethod
    def _info2token(cls, app_info: Auth0AppInfo):
        logger = FoxylibLogger.func_level2logger(
            cls._info2token, logging.DEBUG)

        domain = app_info.api_info.domain
        payload = {'client_id': app_info.client_id,
                   'client_secret': app_info.client_secret,
                   'audience': app_info.api_info.identifier,
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

    class Q:
        @classmethod
        def connection2qitem(cls, connection):
            return f'identities.connection:"{connection}"'

        @classmethod
        def email2qitem(cls, email):
            return f'email:"{email}"'

        @classmethod
        def qitems2q(cls, qitems):
            return " AND " .join(qitems)


    # @classmethod
    # def email_connection2user(cls, app_info: Auth0AppInfo, email, connection):
    #     logger = FoxylibLogger.func_level2logger(cls.email_connection2user,
    #                                              logging.DEBUG)
    #
    #     q = " AND " .join([
    #         f'identities.connection:"{connection}"',
    #         f'email:"{email}"',
    #         ])
    #
    #     logger.debug(pformat({'q': q}))
    #     users = cls.users(app_info, payload={'q': q})
    #
    #     logger.debug(pformat({'users':users}))
    #     user = l_singleton2obj(users, allow_empty_list=True)
    #     return user

    @classmethod
    def q2user(cls, app_info: Auth0AppInfo, q) -> Auth0User:
        logger = FoxylibLogger.func_level2logger(cls.q2user, logging.DEBUG)

        logger.debug(pformat({'q': q}))
        users = cls.users(app_info, payload={'q': q})

        logger.debug(pformat({'users': users}))
        user = l_singleton2obj(users, allow_empty_list=True)
        return user

    @classmethod
    def users(cls, app_info: Auth0AppInfo, payload=None) -> List[Auth0User]:
        logger = FoxylibLogger.func_level2logger(cls.users,
                                                 logging.DEBUG)

        identifier = app_info.api_info.identifier
        token = app_info.token()

        endpoint = f'{identifier}users'

        # logger.debug(pformat({'payload': payload}))

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(endpoint, headers=headers, params=payload)

        logger.debug(pformat({
            'response.url': response.url,
            'response': response, }))

        if not response.ok:
            raise FailedRequest(response)

        j_users = response.json()
        users = [from_dict(Auth0User, j_user) for j_user in j_users]
        return users

    class StatusCode:
        DUPLICATE_USER = 409

    @classmethod
    def delete_user(cls, app_info: Auth0AppInfo, user_id):
        logger = FoxylibLogger.func_level2logger(cls.delete_user,
                                                 logging.DEBUG)

        identifier = app_info.api_info.identifier
        token = app_info.token()
        endpoint = f'{identifier}users/{user_id}'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.delete(endpoint, headers=headers,)

        if not response.ok:
            raise FailedRequest(response)

        return response.ok

    @classmethod
    def delete_users(cls, app_info, user_ids):
        for user_id in user_ids:
            cls.delete_user(app_info, user_id)

    @classmethod
    def create_user(cls, app_info: Auth0AppInfo, body,) -> Auth0User:
        logger = FoxylibLogger.func_level2logger(
            cls.create_user, logging.DEBUG)

        identifier = app_info.api_info.identifier
        token = app_info.token()
        endpoint = f'{identifier}users'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.post(endpoint, headers=headers, json=body)

        logger.debug(pformat({
            'endpoint': endpoint, 'token': token, 'body': body,
            'response': response, }))

        if not response.ok:
            raise FailedRequest(response)

        j_user = response.json()
        logger.debug(pformat({'j_user': j_user, }))
        user = from_dict(Auth0User, j_user)

        return user

    @classmethod
    def create_or_get_user(cls, app_info: Auth0AppInfo, q: str, body) \
            -> Tuple[Auth0User, str]:

        try:
            user = cls.create_user(app_info, body)
            return user, CRUDResult.CREATED
        except FailedRequest as e:
            if e.response.status_code != cls.StatusCode.DUPLICATE_USER:
                raise e

        user = cls.q2user(app_info, q)
        return user, CRUDResult.EXISTING

    @classmethod
    def change_password(cls, app_info: Auth0AppInfo, email):

        domain = app_info.api_info.domain
        payload = {"client_id": app_info.client_id,
                   "email": email,
                   "connection": Auth0Connection.username_password_auth(),
                   }

        endpoint = f'{domain}/dbconnections/change_password'
        response = requests.post(endpoint, json=payload)

        if not response.ok:
            return None

        return response.json()

    @classmethod
    def user_id2ticket_password_change(
            cls, app_info: Auth0AppInfo, user_id, result_url=None):
        """
        reference: https://auth0.com/docs/auth0-email-services/send-email-invitations-for-application-signup
        """
        logger = FoxylibLogger.func_level2logger(
            cls.user_id2ticket_password_change, logging.DEBUG)

        identifier = app_info.api_info.identifier
        token = app_info.token()

        headers = RequestsTool.token2header_bearer(token)

        body = DictTool.nullvalues2excluded({
            "result_url": result_url,
            "user_id": user_id,
            "ttl_sec": 60 * 60 * 2,  # 2 hours
            "mark_email_as_verified": True,
            # "includeEmailInRedirect": False,
            "client_id": app_info.client_id,
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
            raise FailedRequest(response)

        j_response = response.json()
        ticket = j_response['ticket']

        return ticket


class Auth0Connection:
    @classmethod
    def username_password_auth(cls):
        return "Username-Password-Authentication"





