import re

from future.utils import lfilter
from nose.tools import assert_is_not_none

from foxylib.tools.collections.collections_tools import l_singleton2obj
from foxylib.tools.regex.regex_tools import MatchToolkit
from foxylib.tools.string.string_tools import str2strip
from khalalib.chat.chat import KhalaChat


class ChatRole:
    COMMAND = "command"

    class Value:
        COMMAND = "command"
    V = Value

    @classmethod
    def role_class_list(cls):
        return [CommandChatRole]

    @classmethod
    def j_chat2role(cls, chat):
        l_matched = lfilter(lambda x: x.chat2is_role_matched(chat), cls.role_class_list())
        if not l_matched:
            return None

        role_class = l_singleton2obj(l_matched)
        return role_class.NAME



class CommandChatRole:
    PREFIX = "?"
    NAME = ChatRole.V.COMMAND

    @classmethod
    def chat2is_role_matched(cls, chat):
        text = KhalaChat.j_chat2text(chat)
        text_stripped = str2strip(text)

        if not text_stripped: return False;
        if not text_stripped.startswith(cls.PREFIX): return False
        if len(text_stripped)<=1: return False
        return True

    @classmethod
    def chat2command_list(cls, chat):
        text = KhalaChat.j_chat2text(chat)

        m = re.match(r"{}\s*".format(cls.PREFIX), text)
        assert_is_not_none(m)

        i_end = MatchToolkit.match2end(m)

        str_commands = text[i_end:].split(maxsplit=1)[0]
        return str_commands.split(".")

