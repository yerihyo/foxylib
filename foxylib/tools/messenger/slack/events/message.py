# https://api.slack.com/events/message
class MessageEvent:
    NAME = "message"

    class Field:
        TYPE = "type"
        CHANNEL = "channel"
        USER = "user"
        TEXT = "text"
        TS = "ts"
    F = Field

    @classmethod
    def j2channel_id(cls, j):
        return j[cls.F.CHANNEL]

    @classmethod
    def j2user_id(cls, j):
        return j[cls.F.USER]

    @classmethod
    def j2thread_ts(cls, j):
        return j[cls.F.TS]
