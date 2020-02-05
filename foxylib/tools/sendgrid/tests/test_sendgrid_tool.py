import logging
import os
from unittest import TestCase

from sendgrid import SendGridAPIClient

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.sendgrid.sendgrid_tool import MailTool, MailConfig


class TestSendgridTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        j_config = {MailConfig.F.FROM_EMAIL:"yerihyo@gmail.com",
                    MailConfig.F.TO_EMAILS: ["foxytrixy.bot@gmail.com"],
                    MailConfig.F.SUBJECT: "sendgrid test",
                    MailConfig.F.PLAIN_TEXT_CONTENT: "content",
        }
        mail = MailTool.j_config2mail(j_config)

        client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


        response = client.send(mail)
        self.assertEqual(response.status_code, 202)

        # logger.debug({"response.body":response.body,
        #               "response.headers":response.headers,
        #               })