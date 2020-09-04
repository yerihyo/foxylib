# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from datetime import datetime, timedelta

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pytz

from foxylib.tools.collections.collections_tool import l_singleton2obj

from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.json.json_tool import JsonTool

# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class YoutubeapiTool:
    @classmethod
    def credentials2service(cls, credentials):
        return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

