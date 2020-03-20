import os


class FoxylibStripe:
    # @classmethod
    # def client(cls):
    #     stripe.api =
    @classmethod
    def publishable_key(cls):
        return os.environ.get("STRIPE_API_PUBLISHABLE_KEY")

    @classmethod
    def secret_key(cls):
        return os.environ.get("STRIPE_API_SECRET_KEY")
