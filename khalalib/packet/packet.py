import re
from functools import lru_cache

from foxylib.tools.json.json_tool import jdown


class KhalaChat:
    class Field:
        SENDER_ID = "sender_id"
        TEXT = "text"
        CHATROOM_ID = "chatroom_id"
        LOCALE = "locale"

    @classmethod
    def j_chat2sender_id(cls, j_chat): return j_chat[cls.Field.SENDER_ID]

    @classmethod
    def j_chat2text(cls, j_chat): return j_chat[cls.Field.TEXT]

    @classmethod
    def j_chat2chatroom_id(cls, j_chat): return j_chat[cls.Field.CHATROOM_ID]

    @classmethod
    def j_chat2locale(cls, j_chat): return j_chat[cls.Field.LOCALE]

    @classmethod
    @lru_cache(maxsize=2)
    def p_prefix(cls): return re.compile("^\?\s*", re.I)

    @classmethod
    def j_chat2text_body(cls, j_chat):
        text = cls.j_chat2text(j_chat)
        text_body = cls.p_prefix().sub("",text)
        return text_body

    # @classmethod
    # def j_chat2is_respond_req(cls, j_chat):
    #     from khalalib.chat.chat_role import ChatRole
    #     role = ChatRole.j_chat2role(j_chat)
    #     return role is not None

    @classmethod
    def j_chat2command(cls, j_chat):
        text = cls.j_chat2text(j_chat)




class KhalaPacket:
    class Field:
        CHAT = "chat"
        CONTRACT = "contract"


    @classmethod
    def j_chat2j_packet(cls, j_chat):
        j_contract = KhalaContract.j_chat2j_contract(j_chat)

        j = {KhalaPacket.Field.CHAT: j_chat,
             KhalaPacket.Field.CONTRACT: j_contract,
             }
        return j


    @classmethod
    def j_packet2jinni_uuid(cls, j_packet):
        return jdown(j_packet, [cls.Field.CONTRACT, KhalaContract.Field.JINNI_UUID])

    @classmethod
    def j_packet2j_chat(cls, j_packet):
        return jdown(j_packet, [cls.Field.CHAT])

    @classmethod
    def j_packet2j_contract(cls, j_packet):
        return jdown(j_packet, [cls.Field.CONTRACT])


    @classmethod
    def packet2locale(cls, packet):
        j_chat =  cls.j_packet2j_chat(packet)
        locale = KhalaChat.j_chat2locale(j_chat)
        return locale


class KhalaContract:
    class Field:
        ACTION_UUID = "action_uuid"
        JINNI_UUID = "jinni_uuid"
        CONFIG = "config"


    @classmethod
    def j_chat2j_contract(cls, j_chat):
        return {KhalaContract.Field.ACTION_UUID: None,
                KhalaContract.Field.CONFIG: "",
                KhalaContract.Field.JINNI_UUID: None,
                }
