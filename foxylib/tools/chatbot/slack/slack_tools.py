class SlackToolkit:
    @classmethod
    def str2j_block(cls, str_in):
        j = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": str_in,
                },
            }
        return j

    @classmethod
    def j_blocks2h_msg(cls, channel, username, j_blocks):
        h = {
            "channel": channel,
            "username": username,
            "blocks": j_blocks,
        }
        return h