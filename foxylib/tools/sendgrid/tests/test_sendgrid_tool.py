import logging
from unittest import TestCase

import pytest
from sendgrid import Mail

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.sendgrid.sendgrid_tool import SendgridTool, FoxylibSendgrid


class TestSendgridTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason='another test below. skipping to save sendgrid quota')
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        mail = Mail(**{
            'from_email': "yerihyo@gmail.com",
            'to_emails': ["foxytrixy.bot@gmail.com"],
            'subject': "sendgrid test",
            'plain_text_content': "content",
        })

        client = FoxylibSendgrid.client()
        response = client.send(mail)
        self.assertEqual(response.status_code, 202)

        # logger.debug({"response.body":response.body,
        #               "response.headers":response.headers,
        #               })

    def test_02(self):
        # https://www.twilio.com/blog/send-dynamic-emails-python-twilio-sendgrid

        client = FoxylibSendgrid.client()
        mail = Mail(**{
            'from_email': "yerihyo@gmail.com",
            'to_emails': ["foxytrixy.bot@gmail.com"],
        })
        template_id = FoxylibSendgrid.template_id_test()
        data = {
            'Receiver_Nickname': '예리',
            'Sender_Name':'강문영',
            'Sender_Address':'353 Alamo ave',
            'Sender_City': 'Santa Cruz',
            'Sender_State': 'CA',
            'Sender_Zip': '95060',
        }
        response = SendgridTool.template_id2send(
            client, mail, template_id, data)

        self.assertEqual(response.status_code, 202)
