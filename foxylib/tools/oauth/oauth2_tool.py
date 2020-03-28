import os

from nose.tools import assert_true
from oauth2client import file, client, tools, transport


class OAuth2Tool:
    @classmethod
    def scope2credentials(cls,
                          filepath_credentials_json,
                          scopes,
                          filepath_token,
                          http=None,
                          ):
        assert_true(os.path.exists(os.path.dirname(filepath_token)))

        storage = file.Storage(filepath_token)
        if os.path.exists(filepath_token):
            credentials = storage.get()
        else:
            credentials = None

        if not credentials or credentials.invalid:
            if credentials and credentials.expired and credentials.refresh_token:
                if http is None:
                    http = transport.get_http_object()
                credentials.refresh(http)

                storage.put(credentials)
                credentials.set_store(storage)

            else:
                flow = client.flow_from_clientsecrets(filepath_credentials_json, scopes)
                credentials = tools.run_flow(flow, storage)

        return credentials
