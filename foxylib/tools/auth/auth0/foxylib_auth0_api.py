from foxylib.singleton.env.foxylib_env import FoxylibEnv


class FoxylibAuth0API:
    @classmethod
    def endpoint(cls):
        return FoxylibEnv.key2value("AUTH0_TENANT_URL")

    @classmethod
    def audience(cls):
        tenant_url = cls.endpoint()
        return f'{tenant_url}/api/v2/'

    @classmethod
    def identifer(cls):
        return cls.audience()
