import logging
from pprint import pformat

import requests

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool


class Auth0M2MTool:

    @classmethod
    def payload2token(cls, domain, payload):
        logger = FoxylibLogger.func_level2logger(
            cls.payload2token, logging.DEBUG)

        url = f'{domain}/oauth/token'
        response = requests.post(url, json=payload)

        logger.debug(pformat({
            'payload': payload,
            'response':response,
        }))

        j_body = response.json()
        return j_body['access_token']

    # @classmethod
    # def domain2users(cls, domain, token, payload=None):
    #     logger = FoxylibLogger.func_level2logger(cls.domain2users, logging.DEBUG)
    #
    #     endpoint = f'{domain}/api/v2/users'
    #     # logger.debug({'token': token})
    #
    #     headers = RequestsTool.token2header_bearer(token)
    #     response = requests.get(endpoint, headers=headers, params=payload)
    #     users = response.json()
    #
    #     logger.debug(pformat({'users': users, 'response':response,}))
    #
    #     if response.status_code != 200:
    #         return None
    #
    #     return users

    @classmethod
    def users(cls, identifier, token, payload=None):
        logger = FoxylibLogger.func_level2logger(cls.users,
                                                 logging.DEBUG)

        endpoint = f'{identifier}users'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.get(endpoint, headers=headers, params=payload)
        users = response.json()

        logger.debug(pformat({'users': users, 'response': response, }))

        if response.status_code != 200:
            return None

        return users

    @classmethod
    def delete_user(cls, identifier, token, user_id):
        logger = FoxylibLogger.func_level2logger(cls.delete_user,
                                                 logging.DEBUG)

        endpoint = f'{identifier}users/{user_id}'
        # logger.debug({'token': token})

        headers = RequestsTool.token2header_bearer(token)
        response = requests.delete(endpoint, headers=headers,)
        return response.ok

    @classmethod
    def create_user(cls, identifier, token, body,):
        logger = FoxylibLogger.func_level2logger(cls.create_user,
                                                 logging.DEBUG)

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
    def change_password(cls, domain, client_id, email):

        payload = {"client_id": client_id,
                   "email": email,
                   "connection": "Username-Password-Authentication",
                   }

        endpoint = f'{domain}/dbconnections/change_password'
        response = requests.post(endpoint, json=payload)

        if not response.ok:
            return None

        return response.json()



class Auth0Connection:
    @classmethod
    def username_password_auth(cls):
        return "Username-Password-Authentication"
