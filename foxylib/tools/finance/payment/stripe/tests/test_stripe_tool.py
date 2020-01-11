import logging
from unittest import TestCase

import stripe

from foxylib.tools.finance.payment.stripe.foxylib_stripe import FoxylibStripe
from foxylib.tools.finance.payment.stripe.stripe_tool import StripeCharge, StripeTool, StripeCardSample, StripeToken, \
    StripeTokenType, StripeCard
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibStripe(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        secret_key = FoxylibStripe.secret_key()
        # logger.debug({"secret_key": secret_key})

        cardnumber = StripeCardSample.Number.VISA
        j_card_test = StripeCardSample.cardnumber2j_card_test(cardnumber)
        j_token_config = {StripeTool.Config.API_KEY: secret_key,
                          StripeToken.Config.CARD: j_card_test,
                          }
        token = stripe.Token.create(**j_token_config)
        logger.debug({"token": token})

        self.assertFalse(StripeToken.token2livemode(token))
        self.assertEqual(StripeToken.token2type(token), StripeTokenType.V.CARD)

        card_token = StripeToken.token2card(token)
        self.assertEqual(StripeCard.card2last4(card_token), cardnumber[-4:])

        amount = 100
        currency = "usd"
        j_charge_config = {StripeTool.Config.API_KEY: secret_key,
                           StripeCharge.Config.AMOUNT: 100,
                           StripeCharge.Config.CURRENCY: currency,
                           StripeCharge.Config.SOURCE: token,
                           }

        charge = stripe.Charge.create(**j_charge_config)
        logger.debug({"charge": charge})

        self.assertEqual(StripeCharge.charge2amount(charge), amount)
        self.assertEqual(StripeCharge.charge2currency(charge), currency)


