import stripe

from foxylib.tools.env.env_tool import EnvTool


class FoxylibStripe:
    # @classmethod
    # def client(cls):
    #     stripe.api =
    @classmethod
    def publishable_key(cls):
            return EnvTool.k2v("STRIPE_API_PUBLISHABLE_KEY")

    @classmethod
    def secret_key(cls):
        return EnvTool.k2v("STRIPE_API_SECRET_KEY")
