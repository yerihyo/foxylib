from datetime import datetime, timedelta

from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.finance.creditcard.creditcard_tool import CreditcardTool


class StripeTool:
    class Config:
        API_KEY = "api_key"

class StripeCard:
    class Config:
        EXP_MONTH = "exp_month"
        EXP_YEAR = "exp_year"
        NUMBER = "number"
        CURRENCY = "currency"
        CVC = "cvc"

    class Field:
        ID = "id"
        EXP_MONTH = "exp_month"
        EXP_YEAR = "exp_year"
        LAST4 = "last4"
        BRAND = "brand"
    F = Field

    @classmethod
    def card2exp_month(cls, card):
        return card.get(cls.F.EXP_MONTH)

    @classmethod
    def card2exp_year(cls, card):
        return card.get(cls.F.EXP_YEAR)

    @classmethod
    def card2last4(cls, card):
        return card.get(cls.F.LAST4)

    @classmethod
    def card2brand(cls, card):
        return card.get(cls.F.BRAND)


class StripeCardSample:
    class Number:
        VISA = "4242424242424242"

    @classmethod
    def expire_month_year_future(cls):
        dt_future = datetime.now() + timedelta(days=365)
        str_month = dt_future.strftime("%m")
        str_year = dt_future.strftime("%y")
        return (str_month, str_year)

    @classmethod
    def cardnumber2j_card_test(cls, cardnumber):
        exp_month, exp_year = cls.expire_month_year_future()
        cvc_digit = CreditcardTool.cardnumber2cvc_digit(cardnumber)
        cvc = "9"*cvc_digit

        j = {StripeCard.Config.EXP_MONTH:exp_month,
             StripeCard.Config.EXP_YEAR: exp_year,
             StripeCard.Config.NUMBER: cardnumber,
             StripeCard.Config.CVC: cvc,
             }
        return j


class StripeTokenType:
    class Value:
        CARD = "card"
    V = Value

class StripeToken:
    class Config:
        CARD = "card"

    class Field:
        ID = "id"
        LIVEMODE = "livemode"
        TYPE = "type"
        CARD = "card"
    F = Field

    @classmethod
    def token2livemode(cls, token):
        return token[cls.F.LIVEMODE]

    @classmethod
    def token2type(cls, token):
        return token[cls.F.TYPE]

    @classmethod
    def token2card(cls, token):
        return token.get(cls.F.CARD)



class StripeCharge:
    class Config:
        AMOUNT = "amount"
        CURRENCY = "currency"
        SOURCE = "source"

        APPLICATION_FEE_AMOUNT = "application_fee_amount"
        DESCRIPTION = "description"

    class Field:
        AMOUNT = "amount"
        CURRENCY = "currency"
    F = Field

    @classmethod
    def charge2amount(cls, charge):
        return charge.get(cls.F.AMOUNT)

    @classmethod
    def charge2currency(cls, charge):
        return charge.get(cls.F.CURRENCY)



class FoxylibStripe:
    @classmethod
    def publishable_key(cls):
        return EnvTool.k2v("STRIPE_API_PUBLISHABLE_KEY")

    @classmethod
    def secret_key(cls):
        return EnvTool.k2v("STRIPE_API_SECRET_KEY")

