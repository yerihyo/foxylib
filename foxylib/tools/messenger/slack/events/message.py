# https://api.slack.com/events/message
class MessageEvent:
    NAME = "message"

    class Field:
        TYPE = "type"
        CHANNEL = "channel"
        USER = "user"
        TEXT = "text"
        TS = "ts"


    @classmethod
    def j2channel_id(cls, j):
        return j[cls.Field.CHANNEL]

    @classmethod
    def j2user_id(cls, j):
        return j[cls.Field.USER]

    @classmethod
    def j2thread_ts(cls, j):
        return j[cls.Field.TS]
