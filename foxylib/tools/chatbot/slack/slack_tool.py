from nose.tools import assert_true

from foxylib.tools.string.string_tools import str2strip, str2lower


class SlackTool:
    @classmethod
    def str2j_block_list(cls, str_in):
        l = str_in.splitlines()
        n = len(l)
        p = 20
        k = n // p + (1 if n % p else 0)

        j_list = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(l[i * p:(i + 1) * p]),
            },
        } for i in range(k)]
        return j_list

    @classmethod
    def j_blocks2h_msg(cls, channel, username, j_blocks):
        h = {
            "channel": channel,
            "username": username,
            "blocks": j_blocks,
        }
        return h

    @classmethod
    def h_payload2text(cls, h): return h["data"].get("text")

    @classmethod
    def h_payload2channel(cls, h): return h["data"].get("channel")

    @classmethod
    def h_payload2web_client(cls, h): return h["web_client"]

    @classmethod
    def str_in2str_cmd_body(cls, str_in):
        str_clean = str2lower(str2strip(str_in))
        if not str_clean: return None

        l = str_clean.split(maxsplit=1)
        assert_true(l)

        str_cmd = l[0]
        str_body = l[1] if len(l)>1 else None
        return (str_cmd, str_body,)