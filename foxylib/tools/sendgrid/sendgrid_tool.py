import logging
import os
from functools import lru_cache

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from sendgrid import SendGridAPIClient

from foxylib.tools.log.foxylib_logger import FoxylibLogger


# class MailConfig:
#     FROM_EMAIL = "from_email"
#     TO_EMAILS = "to_emails"
#     SUBJECT = "subject"
#
#     PLAIN_TEXT_CONTENT = "plain_text_content"
#     HTML_CONTENT = "html_content"
from foxylib.tools.network.requests.requests_tool import FailedRequest


class SendgridTool:
    # @classmethod
    # def config2mail(cls, config, ):
    #     return Mail(**config)
    #
    # @classmethod
    # def config2send(cls, client, config, ):
    #     mail = cls.config2mail(config)
    #     response = client.send(mail)
    #     return response

    @classmethod
    def response2is_ok(cls, response):
        return response.status_code in {202}

    @classmethod
    def template_id2send(cls, client, mail, template_id, data,):
        logger = FoxylibLogger.func_level2logger(
            cls.template_id2send, logging.DEBUG)

        mail.template_id = template_id
        mail.dynamic_template_data = data

        try:
            response = client.send(mail)
        except Exception as error:
            logger.error({'error':error})
            raise error

        if not cls.response2is_ok(response):
            raise FailedRequest(response)

        return response


    # @classmethod
    # def SendDynamic(cls):
    #     """ Send a dynamic email to a list of email addresses
    #
    #     :returns API response code
    #     :raises Exception e: raises an exception """
    #     # create Mail object and populate
    #     message = Mail(
    #         from_email=FROM_EMAIL,
    #         to_emails=TO_EMAILS)
    #     # pass custom values for our HTML placeholders
    #     message.dynamic_template_data = {
    #         'subject': 'SendGrid Development',
    #         'place': 'New York City',
    #         'event': 'Twilio Signal'
    #     }
    #     message.template_id = TEMPLATE_ID
    #     # create our sendgrid client object, pass it our key, then send and return our response objects
    #     try:
    #         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    #         response = sg.send(message)
    #         code, body, headers = response.status_code, response.body, response.headers
    #         print(f"Response code: {code}")
    #         print(f"Response headers: {headers}")
    #         print(f"Response body: {body}")
    #         print("Dynamic Messages Sent!")
    #     except Exception as e:
    #         print("Error: {0}".format(e))
    #     return str(response.status_code)


class FoxylibSendgrid:
    @classmethod
    def api_key(cls):
        logger = FoxylibLogger.func_level2logger(cls.api_key, logging.DEBUG)

        api_key = FoxylibEnv.key2value('SENDGRID_API_KEY')
        # logger.debug({'api_key':api_key})

        return api_key

    @classmethod
    @lru_cache(maxsize=2)
    def client(cls):
        return SendGridAPIClient(cls.api_key())

    @classmethod
    def template_id_test(cls):
        return 'd-ef0822fd06634582a0559540318a8afd'
