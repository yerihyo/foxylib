from foxylib.tools.url.url_tool import URLTool


class DiscordTool:
    @classmethod
    def str2url_escaped(cls, str_in):
        str_out = URLTool.pattern().sub(r'<\1>', str_in)
        return str_out

    @classmethod
    def user_message2is_author(cls, user, message):
        return message.author == user
