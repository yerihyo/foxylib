import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class MailConfig:
    class Field:
        FROM_EMAIL = "from_email"
        TO_EMAILS = "to_emails"
        SUBJECT = "subject"

        PLAIN_TEXT_CONTENT = "plain_text_content"
        HTML_CONTENT = "html_content"


class MailTool:
    @classmethod
    def j_config2mail(cls, j_config, ):
        return Mail(**j_config)

    @classmethod
    def j_config2send(cls, client, j_config, ):
        mail = cls.j_config2mail(j_config)
        response = client.send(mail)
        return response

        # try:
        #     response = client.send(mail)
        #     print(response.status_code)
        #     print(response.body)
        #     print(response.headers)
        # except Exception as e:
        #     print(e.message)