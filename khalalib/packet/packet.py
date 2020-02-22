from foxylib.tools.json.json_tool import jdown
from khalalib.chat.chat import KhalaChat


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
    def j_packet2locale(cls, j_packet):
        j_chat =  cls.j_packet2j_chat(j_packet)
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