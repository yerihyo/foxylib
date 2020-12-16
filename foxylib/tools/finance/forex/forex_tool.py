from decimal import Decimal
from functools import lru_cache

from forex_python.converter import CurrencyRates
from nose.tools import assert_true


class Forex:
    class Field:
        CURRENCY = "currency"
        DECIMAL = "decimal"

    @classmethod
    def pair2forex(cls, currency, decimal):
        assert_true(isinstance(currency, str))

        forex = {cls.Field.CURRENCY: currency,
                 cls.Field.DECIMAL: decimal,
                 }
        return forex

    @classmethod
    def forex2str(cls, forex):
        currency = forex[cls.Field.CURRENCY]
        assert_true(isinstance(currency, str))

        decimal = forex[cls.Field.DECIMAL]
        return "{} {}".format(currency, decimal)

    @classmethod
    def parse(cls, str_in):
        currency, str_decimal = str_in.split(maxssplit=1)
        forex = {cls.Field.CURRENCY:currency,
                 cls.Field.DECIMAL: Decimal(str_decimal),
                 }
        return forex


class ForexTool:
    @classmethod
    @lru_cache(maxsize=2)
    def cr(cls):
        return CurrencyRates(force_decimal=True)

    @classmethod
    def convert(cls, forex, currency):
        forex_in, currency_out = forex, currency

        currency_in = forex_in[Forex.Field.CURRENCY]
        decimal_in = forex_in[Forex.Field.DECIMAL]
        decimal_out = cls.cr().convert(currency_in, currency_out, decimal_in)

        forex_out = {Forex.Field.CURRENCY: currency_out,
                     Forex.Field.DECIMAL: decimal_out,
                     }
        return forex_out

    @classmethod
    def forex2currency(cls, forex_in, currency):
        forex_out = cls.convert(forex_in, currency)
        amount_out = forex_out[Forex.Field.DECIMAL]
        return amount_out
