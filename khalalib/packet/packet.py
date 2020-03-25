import re
from functools import lru_cache

from foxylib.tools.json.json_tool import jdown


class KhalaPacket:
    class Field:
        TEXT = "text"
        LOCALE = "locale"

        # SENDER_ID = "sender_id"
        # TYPE = "type"
        # CHATROOM_ID = "chatroom_id"

    @classmethod
    def packet2text(cls, j_chat): return j_chat[cls.Field.TEXT]

    @classmethod
    def packet2locale(cls, j_chat): return j_chat[cls.Field.LOCALE]







