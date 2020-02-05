import re
from functools import lru_cache

from foxylib.tools.function.function_tool import FunctionTool


class CreditcardCompany:
    class Value:
        VISA = "visa"
        MASTERCARD = "mastercard"
        DISCOVER = "discover"
        AMEX = "amex"
        DINERSCLUB = "dinersclub"
        ETC = "etc"
    V = Value

    # https://www.regular-expressions.info/creditcard.html
    @classmethod
    def rstr_visa(cls):
        return r"4[0-9]{12}(?:[0-9]{3})?"

    @classmethod
    def rstr_mastercard(cls):
        return r"(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}"

    @classmethod
    def rstr_amex(cls):
        return r"3[47][0-9]{13}"

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_amex(cls):
        return re.compile(cls.rstr_amex())

    @classmethod
    def rstr_dinersclub(cls):
        return r"3(?:0[0-5]|[68][0-9])[0-9]{11}"

    @classmethod
    def rstr_discover(cls):
        return r"6(?:011|5[0-9]{2})[0-9]{12}"

    @classmethod
    def rstr_jcb(cls):
        return r"(?:2131|1800|35\d{3})\d{11}"



class CreditcardTool:
    @classmethod
    def cardnumber2cvc_digit(cls, cardnumber):
        if CreditcardCompany.pattern_amex().match(cardnumber):
            return 4
        return 3

    # @classmethod
    # def cardnumber2company(cls, cardnumber):
    #     if cardnumber[0] == "4":
#             return CreditcardCompany.V.VISA
#
#         if cardnumber[1] == "5":
#             return CreditcardCompany.V.MASTERCARD
#
#         if cardnumber[0] == "6":
#             return CreditcardCompany.V.DISCOVER
#
#         if cardnumber[:2] == "37":
#             return CreditcardCompany.V.AMEX
#
#         "300-305, 54-55, 38-39, 2014, 36"
#
