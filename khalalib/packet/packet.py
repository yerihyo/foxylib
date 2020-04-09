import re
from functools import lru_cache

from foxylib.tools.json.json_tool import jdown


class KhalaPacket:
    class Field:
        TEXT = "text"
        LOCALE = "locale"
        CHANNEL = "channel"
        EXTRA = "extra"


        # SENDER_ID = "sender_id"
        # TYPE = "type"
        # CHATROOM_ID = "chatroom_id"

    @classmethod
    def packet2text(cls, packet):
        return packet[cls.Field.TEXT]

    @classmethod
    def packet2locale(cls, packet):
        return packet[cls.Field.LOCALE]

    @classmethod
    def packet2channel(cls, packet):
        return packet[cls.Field.CHANNEL]

    @classmethod
    def packet2extra(cls, packet):
        return packet[cls.Field.EXTRA]

    # @classmethod
    # def packet2channel_user_id(cls, packet):
    #     return packet[cls.Field.CHANNEL_USER_ID]







