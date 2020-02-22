import re
from functools import lru_cache

from foxylib.tools.string.string_tool import str2strip


class KhalaChat:
    class Field:
        SENDER_ID = "sendier_id"
        TEXT = "text"
        CHATROOM_ID = "chatroom_id"
        LOCALE = "locale"


    class Builder:
        @classmethod
        def user_id2h(cls, user_id,): return {KhalaChat.Field.SENDER_ID:user_id,}
        @classmethod
        def text2h(cls, text): return {KhalaChat.Field.TEXT: text,}
        @classmethod
        def chatroom_id2h(cls, ck): return {KhalaChat.Field.CHATROOM_ID: ck}

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

    @classmethod
    def j_chat2is_respond_req(cls, j_chat):
        from khalalib.chat.chat_role import ChatRole
        role = ChatRole.j_chat2role(j_chat)
        return role is not None

    @classmethod
    def j_chat2command(cls, j_chat):
        text = cls.j_chat2text(j_chat)


