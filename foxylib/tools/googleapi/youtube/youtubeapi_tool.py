# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import googleapiclient.discovery
import googleapiclient.errors


# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class YoutubeapiTool:
    @classmethod
    def credentials2service(cls, credentials):
        return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials, cache_discovery=False)

