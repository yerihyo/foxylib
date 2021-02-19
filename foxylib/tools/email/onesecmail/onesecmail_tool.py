import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import requests
from dacite import from_dict
from dateutil.parser import parse
from future.utils import lmap

from foxylib.tools.collections.collections_tool import DictTool, l_singleton2obj
from foxylib.tools.dataclass.dataclass_tool import DataclassTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import URLTool


@dataclass
class Snippet:
    id: int
    from_: str
    subject: str
    date: datetime

    @classmethod
    def json2dict(cls, j_message):
        j_remapped = DictTool.keys2remapped(j_message, {'from': 'from_'})

        pinpoint_tree = {
            DataclassTool.fieldname2checked(cls, 'date'): parse,
        }
        h_message = JsonTool.convert_pinpoint(j_remapped, pinpoint_tree)
        return h_message

    @classmethod
    def from_json(cls, j_message):
        return from_dict(cls, cls.json2dict(j_message))


@dataclass
class Attachment:
    filename: str
    contentType: str
    size: int


@dataclass
class Message(Snippet):
    attachments: List[Attachment]
    body: str
    textBody: str
    htmlBody: str

    @classmethod
    def from_json(cls, j_message):
        return from_dict(cls, Snippet.json2dict(j_message))


class OnesecmailTool:
    """
    https://www.1secmail.com/api/
    """

    @classmethod
    def endpoint(cls):
        return "https://www.1secmail.com/api/v1/"


    @classmethod
    def create_emails(cls, count=None):
        logger = FoxylibLogger.func_level2logger(cls.create_emails, logging.DEBUG)

        params = DictTool.nullvalues2excluded({
            'action': 'genRandomMailbox',
            'count': count,
        })
        url = URLTool.append_query2url(cls.endpoint(), params)
        response = requests.get(url)
        if not response.ok:
            return None

        # logger.debug({'url':url,'response.text':response.text})

        emails = response.json()
        return emails

    @classmethod
    def create_email(cls):
        emails = cls.create_emails(count=1)
        if emails is None:
            return None

        return l_singleton2obj(emails)

    @classmethod
    def email2snippets(cls, email) -> Optional[List[Snippet]]:
        logger = FoxylibLogger.func_level2logger(
            cls.email2snippets, logging.DEBUG)

        login, domain = email.split("@")
        params = {'action': 'getMessages', 'login': login, 'domain': domain, }
        url = URLTool.append_query2url(cls.endpoint(), params)
        # logger.debug({'url':url})

        response = requests.get(url)
        if not response.ok:
            return None

        snippets = lmap(Snippet.from_json, response.json())
        logger.debug({#'response': response,
                      #'response.text': response.text,
                      'snippets':snippets,
                      })

        return snippets

    @classmethod
    def message_id2message(cls, email, message_id) -> Optional[Message]:
        logger = FoxylibLogger.func_level2logger(
            cls.message_id2message, logging.DEBUG)

        login, domain = email.split("@")
        params = {'action': 'readMessage', 'login': login, 'domain': domain,
                  'id': message_id}
        url = URLTool.append_query2url(cls.endpoint(), params)
        logger.debug({'url': url})

        response = requests.get(url)
        if not response.ok:
            return None

        message = Message.from_json(response.json())
        return message

