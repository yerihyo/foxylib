from foxylib.tools.json.json_tools import jdown


class KhalaPacket:
    class Field:
        CHAT = "chat"
        CONTRACT = "contract"
    F = Field

    @classmethod
    def j_chat2j_packet(cls, j_chat):
        j_contract = KhalaContract.j_chat2j_contract(j_chat)

        j = {KhalaPacket.F.CHAT: j_chat,
             KhalaPacket.F.CONTRACT: j_contract,
             }
        return j


    @classmethod
    def j_packet2jinni_uuid(cls, j_packet):
        return jdown(j_packet, [cls.F.CONTRACT, KhalaContract.F.JINNI_UUID])

    @classmethod
    def j_packet2j_chat(cls, j_packet):
        return jdown(j_packet, [cls.F.CHAT])


class KhalaContract:
    class Field:
        ACTION_UUID = "action_uuid"
        JINNI_UUID = "jinni_uuid"
        CONFIG = "config"
    F = Field

    @classmethod
    def j_chat2j_contract(cls, j_chat):
        return {KhalaContract.F.ACTION_UUID: None,
                KhalaContract.F.CONFIG: "",
                KhalaContract.F.JINNI_UUID: None,
                }