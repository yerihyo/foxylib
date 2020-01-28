import logging
from decimal import Decimal
from unittest import TestCase

import stripe

from foxylib.tools.finance.payment.stripe.foxylib_stripe import FoxylibStripe
from foxylib.tools.finance.payment.stripe.stripe_tool import StripeCharge, StripeTool, StripeCardSample, StripeToken, \
    StripeTokenType, StripeCard, StripeAnalysis
from foxylib.tools.finance.tax.korea.korea_tax_tool import KoreaTaxTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestFoxylibStripe(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self): # charge
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


    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        def v_pair2j_analysis(v_charged, v_rawprice):
            v_vat_removed = KoreaTaxTool.charged2vat_removed(v_charged)
            j_analysis = StripeAnalysis.charged_rawprice2j_analysis(v_vat_removed, v_rawprice)
            return j_analysis

        hyp1 = v_pair2j_analysis(Decimal("1.50"), Decimal("1.00"))
        ref1 = {'profit_absolute': '0.03', 'profit_ratio': '0.0337'}

        logger.debug({"hyp1":hyp1})
        self.assertEqual(hyp1, ref1)



        hyp2 = v_pair2j_analysis(Decimal("6.20"), Decimal("5.00"))
        ref2 = {'profit_absolute': '0.19', 'profit_ratio': '0.0372'}

        logger.debug({"hyp2": hyp2})
        self.assertEqual(hyp2, ref2)



        hyp3 = v_pair2j_analysis(Decimal("12.00"), Decimal("10.00"))
        ref3 = {'profit_absolute': '0.31', 'profit_ratio': '0.0310'}

        logger.debug({"hyp3": hyp3})
        self.assertEqual(hyp3, ref3)


    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        def rawprice_profitratio2final(v_rawprice, ratio_profit):
            v_stripe = StripeTool.rawprice_profitratio2charged(v_rawprice, ratio_profit)

            v_vat_added = KoreaTaxTool.price2vat_added(v_stripe)

            logger.debug({"v_rawprice":v_rawprice,
                          "ratio_profit":ratio_profit,
                          "v_stripe":v_stripe,
                          "v_vat_added":v_vat_added,
                          })
            return v_vat_added


        hyp1 = rawprice_profitratio2final(Decimal("1.00"),Decimal("0.10"))
        ref1 = Decimal('1.57509')

        logger.debug({"hyp1":hyp1})
        self.assertEqual(hyp1, ref1)

        hyp2 = rawprice_profitratio2final(Decimal("5.00"),Decimal("0.10"))
        ref2 = Decimal('6.55545')

        logger.debug({"hyp2": hyp2})
        self.assertEqual(hyp2, ref2)

        hyp3 = rawprice_profitratio2final(Decimal("10.0"),Decimal("0.10"))
        ref3 = Decimal('12.7809')

        logger.debug({"hyp3": hyp3})
        self.assertEqual(hyp3, ref3)




        hyp4 = rawprice_profitratio2final(Decimal("1.00"), Decimal("0.05"))
        ref4 = Decimal('1.518495')

        logger.debug({"hyp4": hyp4})
        self.assertEqual(hyp4, ref4)

        hyp5 = rawprice_profitratio2final(Decimal("5.00"), Decimal("0.05"))
        ref5 = Decimal('6.272475')

        logger.debug({"hyp5": hyp5})
        self.assertEqual(hyp5, ref5)

        hyp6 = rawprice_profitratio2final(Decimal("10.0"), Decimal("0.05"))
        ref6 = Decimal('12.21495')

        logger.debug({"hyp6": hyp6})
        self.assertEqual(hyp6, ref6)
