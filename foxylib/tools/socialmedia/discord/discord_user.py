class DiscordUser:
    class Field:
        ID = "id"
        USERNAME = "username"

    @classmethod
    def user2id(cls, user):
        return user.get(cls.Field.ID)

    @classmethod
    def user2username(cls, user):
        return user.get(cls.Field.USERNAME)
