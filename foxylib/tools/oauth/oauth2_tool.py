import logging
import os
from functools import reduce

from nose.tools import assert_true
from oauth2client import file, client, tools, transport

from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)

class OAuth2Tool:
    # @classmethod
    # def scope2credentials(cls,
    #                       filepath_credentials_json,
    #                       scopes,
    #                       filepath_token,
    #                       http=None,
    #                       ):
    #     assert_true(os.path.exists(os.path.dirname(filepath_token)))
    #
    #     storage = file.Storage(filepath_token)
    #     if os.path.exists(filepath_token):
    #         credentials = storage.get()
    #     else:
    #         credentials = None
    #
    #     if not credentials or credentials.invalid:
    #         if credentials and credentials.expired and credentials.refresh_token:
    #             if http is None:
    #                 http = transport.get_http_object()
    #             credentials.refresh(http)
    #
    #             storage.put(credentials)
    #             credentials.set_store(storage)
    #
    #         else:
    #             flow = client.flow_from_clientsecrets(filepath_credentials_json, scopes)
    #             credentials = tools.run_flow(flow, storage)
    #
    #     return credentials

    @classmethod
    def creator_refresher_readwriter2credentials(cls, f_create, f_refresh, readwriter):
        """
        reference: https://developers.google.com/people/quickstart/python
        """

        logger = FoxylibLogger.func_level2logger(
            cls.creator_refresher_readwriter2credentials, logging.DEBUG)

        creds = readwriter.read()
        logger.debug({'creds': creds})

        if creds and creds.valid:
            logger.debug({'creds.valid': creds.valid})
            return creds

        if creds and creds.expired and creds.refresh_token:
            creds = f_refresh(creds)
        else:
            creds = f_create()

        readwriter.write(creds)
        return creds
