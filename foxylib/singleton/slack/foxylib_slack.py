# https://pypi.org/project/slackclient/

import logging
import os
from functools import lru_cache, partial

from slack import RTMClient, WebClient

from foxylib.singleton.env.foxylib_env import FoxylibEnv
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.messenger.slack.slack_tool import SlackTool
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.function.function_tool import FunctionTool


class FoxylibSlack:
    @classmethod
    def xoxb_token(cls):
        logger = FoxylibLogger.func_level2logger(cls.xoxb_token, logging.DEBUG)

        token = FoxylibEnv.key2value("SLACK_BOT_USER_OAUTH_ACCESS_TOKEN")
        # logger.debug({"token": token})

        return token

    @classmethod
    def xoxp_token(cls):
        logger = FoxylibLogger.func_level2logger(cls.xoxp_token, logging.DEBUG)

        token = FoxylibEnv.key2value("SLACK_OAUTH_ACCESS_TOKEN")
        # logger.debug({"token": token})

        return token

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def rtm_client(cls):
        return SlackTool.token2rtm_client(cls.xoxb_token())

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def web_client(cls):
        return SlackTool.token2web_client(cls.xoxb_token())


class FoxylibChannel:
    class Value:
        FOXYLIB = "foxylib"
    V = Value
