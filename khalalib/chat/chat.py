from foxylib.tools.string.string_tools import str2strip


class Chat:
    class Key:
        SENDER_UUID = "sender_uuid"
        TEXT = "text"
        CHATROOM_KEY = "chatroom_key"

    K = Key

    class H:
        @classmethod
        def user_uuid2h(cls, user_uuid,): return {Chat.K.SENDER_UUID:user_uuid,}
        @classmethod
        def text2h(cls, text): return {Chat.K.TEXT: text,}
        @classmethod
        def chatroom_key2h(cls, ck): return {Chat.K.CHATROOM_KEY: ck}


    @classmethod
    def chat2sender_uuid(cls, chat): return chat[cls.K.SENDER_UUID]
    @classmethod
    def chat2text(cls, chat): return chat[cls.K.TEXT]
    @classmethod
    def chat2chatroom_key(cls, chat): return chat[cls.K.CHATROOM_KEY]

    @classmethod
    def chat2is_respond_req(cls, chat):
        from khalalib.chat.chat_role import ChatRole
        role = ChatRole.j_chat2role(chat)
        return role is not None

    @classmethod
    def chat2command(cls, chat):
        text = cls.chat2text(chat)


