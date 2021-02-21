import logging
import time
from unittest import TestCase

from sendgrid import Mail, Email, To, Content, PlainTextContent

from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.datetime.datetime_tool import DatetimeTool
from foxylib.tools.email.onesecmail.onesecmail_tool import OnesecmailTool, \
    Snippet, Message
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.sendgrid.sendgrid_tool import FoxylibSendgrid


class TestOnesecmailTool(TestCase):
    """
    https://www.1secmail.com/api/
    """

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        from_email, to_email = OnesecmailTool.create_emails(count=2)
        logger.debug({'from_email': from_email, 'to_email':to_email})

        dt_pivot = DatetimeTool.utc_now_milli()
        subject = f"TestOnesecmailTool.test_01() - {dt_pivot.isoformat()}"
        content = Content("text/plain", "content")
        plain_text_content = PlainTextContent("content")
        j_mail = {
            'from_email': Email(from_email, 'Fake Sender'),
            'to_emails': [To(to_email, "Fake Receiver")],
            'subject': subject,
            'plain_text_content': plain_text_content,
        }
        mail = Mail(**j_mail)

        client = FoxylibSendgrid.client()
        client.send(mail)
        logger.debug({'stage':'mail sent'})
        time.sleep(3)

        snippets = OnesecmailTool.email2snippets(to_email)
        snippet: Snippet = IterTool.filter2singleton(
            lambda s: s.subject == subject, snippets)

        message: Message = OnesecmailTool.message_id2message(
            to_email, snippet.id)

        self.assertEqual(message.subject, subject)
