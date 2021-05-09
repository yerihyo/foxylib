import logging
from dataclasses import dataclass
from datetime import datetime
from pprint import pformat
from typing import Tuple, List

import dateutil.parser
import requests
from dacite import from_dict
from future.utils import lmap
from nose.tools import assert_is_not_none

from foxylib.tools.auth.auth0.auth0_tool import Auth0AppInfo
from foxylib.tools.collections.collections_tool import l_singleton2obj, \
    DictTool, ListTool
from foxylib.tools.database.crud_tool import CRUDResult
from foxylib.tools.dataclass.dataclass_tool import DataclassTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool, \
    FailedRequest


@dataclass
class Auth0User:
    user_id: str
    email_verified: bool
    email: str
    name: str
    nickname: str
    picture: str
    updated_at: datetime

    @classmethod
    def fn2chkd(cls, fieldname):
        return DataclassTool.fieldname2checked(cls, fieldname)

    @classmethod
    def jdoc2hdoc(cls, jdoc_in):
        transducer_tree = {
            cls.fn2chkd('updated_at'): dateutil.parser.parse,
        }

        hdoc_out = JsonTool.transduce_value(jdoc_in, transducer_tree)
        return DictTool.emptyvalues2excluded(hdoc_out)

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
        class Delim:
            AND = "AND"
            OR = "OR"

        @classmethod
        def connection2q(cls, connection):
            return f'identities.connection:"{connection}"'

        @classmethod
        def email2q(cls, email):
            return f'email:{email}'

        @classmethod
        def email_domain2q(cls, domain):
            return f'email:*@{domain}'

        @classmethod
        def qs2joined(cls, qs, delim):
            if not qs:
                return None

            return f" {delim} ".join(map(lambda q: f'({q})', qs))

        @classmethod
        def qs2and(cls, qs):
            return cls.qs2joined(qs, cls.Delim.AND)

        @classmethod
        def qs2or(cls, qs):
            return cls.qs2joined(qs, cls.Delim.OR)

    @classmethod
    def q2users(cls, app_info: Auth0AppInfo, q) -> List[Auth0User]:
        logger = FoxylibLogger.func_level2logger(cls.q2users, logging.DEBUG)

        logger.debug(pformat({'q': q}))
        payload = {'q': q} if q else None
        users = cls.users(app_info, payload=payload)
        return users

    @classmethod
    def q2user(cls, app_info: Auth0AppInfo, q) -> Auth0User:
        users = cls.q2users(app_info,q)
        user = l_singleton2obj(users, allow_empty_list=True)
        return user

    @classmethod
    def user_id2user(cls, app_info: Auth0AppInfo, user_id: str) -> Auth0User:
        logger = FoxylibLogger.func_level2logger(
            cls.user_id2user, logging.DEBUG)

        assert_is_not_none(user_id)

        identifier = app_info.api_info.identifier
        token = app_info.token()

        endpoint = f'{identifier}users/{user_id}'

        # logger.debug(pformat({'payload': payload}))

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(endpoint, headers=headers)

        logger.debug(pformat({
            'response.url': response.url,
            'response': response, }))

        if not response.ok:
            raise FailedRequest(response)

        j_user = response.json()
        user = from_dict(Auth0User, Auth0User.jdoc2hdoc(j_user))
        return user

    @classmethod
    def users(cls, app_info: Auth0AppInfo, payload=None) -> List[Auth0User]:
        logger = FoxylibLogger.func_level2logger(
            cls.users, logging.DEBUG)

        identifier = app_info.api_info.identifier
        token = app_info.token()

        # https://auth0.com/docs/api/management/v2/#!/Users/get_users
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
        logger.debug(pformat({'j_users':j_users}))
        users = [from_dict(Auth0User, Auth0User.jdoc2hdoc(j_user)) for j_user in j_users]
        return users

    class StatusCode:
        DUPLICATE_USER = 409

    @classmethod
    def delete_user(cls, app_info: Auth0AppInfo, user_id: str):
        logger = FoxylibLogger.func_level2logger(
            cls.delete_user, logging.DEBUG)

        identifier = app_info.api_info.identifier
        token = app_info.token()
        endpoint = f'{identifier}users/{user_id}'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.delete(endpoint, headers=headers,)

        logger.debug(pformat({
            'response':response,
            # 'response.text': response.text,
            'user_id':user_id,
            'response.url':response.url,
        }))

        if not response.ok:
            raise FailedRequest(response)

        return response.ok

    @classmethod
    def delete_users(cls, app_info: Auth0AppInfo, user_ids: List[str]):
        for i, user_id in enumerate(user_ids):
            is_success = cls.delete_user(app_info, user_id)
            if is_success:
                yield i

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
        user = from_dict(Auth0User, Auth0User.jdoc2hdoc(j_user))

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

        users = cls.q2users(app_info, q)
        user = l_singleton2obj(users, allow_empty_list=True)
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

            #### should not be there for result_url
            # https://auth0.com/docs/api/management/v2#!/Tickets/post_password_change
            # "client_id": app_info.client_id,
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

    @classmethod
    def emails2deleted(cls, app_info: Auth0AppInfo, emails):
        q = Auth0M2MTool.Q.qs2or(map(Auth0M2MTool.Q.email2q, emails))
        users = Auth0M2MTool.q2users(app_info, q)
        user_ids = [user.user_id for user in users]
        indexes_deleted = Auth0M2MTool.delete_users(app_info, user_ids)

        users_deleted: List[Auth0User] = ListTool.indexes2filtered(
            users, indexes_deleted)
        emails_deleted = lmap(lambda u: u.email, users_deleted)
        return emails_deleted


class Auth0Connection:
    @classmethod
    def username_password_auth(cls):
        return "Username-Password-Authentication"





