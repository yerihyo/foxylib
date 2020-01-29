import logging
import re
from functools import lru_cache

import requests

from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.string.string_tool import format_str

from foxylib.tools.url.url_tool import URLTool


class YoutubeTool:
    # @classmethod
    # def url2video_id(cls, url):
    #     h_query = URLTool.url2h_query(url)
    #     l = h_query.get("v")
    #     return l_singleton2obj(l)

    @classmethod
    def video_id2url(cls, video_id):
        url_base = "https://www.youtube.com/watch"
        h = {"v":video_id}
        url = URLTool.append_query2url(url_base, h)
        return url

    @classmethod
    def url2is_accessible(cls, url):
        httpr = requests.head(url)
        return httpr.ok

    @classmethod
    def rstr_video_id(cls):
        return r"[A-Za-z0-9\-=_]{11}"

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_video_id(cls):
        return re.compile(cls.rstr_video_id())

    @classmethod
    def rstr_url_prefix(cls):
        return r'(?:https?://)?(?:www\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)/(?:watch\?v=|embed/|v/|.+\?v=)?'

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_url_prefix(cls):
        return re.compile(cls.rstr_url_prefix())

    @classmethod
    def rstr_url(cls, ):
        logger = FoxylibLogger.func_level2logger(cls.rstr_url, logging.DEBUG)

        rstr_prefix = cls.rstr_url_prefix()
        rstr_video_id = cls.rstr_video_id()
        rstr = RegexTool.join("", [rstr_prefix, rstr_video_id])

        logger.debug({"rstr": rstr})
        return rstr

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_url(cls):
        return re.compile(cls.rstr_url())

    # @classmethod
    # @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    # def _pattern_url2video_id(cls, ):
    #     logger = FoxylibLogger.func_level2logger(cls.rstr_url, logging.DEBUG)
    #
    #     rstr_prefix = cls.rstr_url_prefix()
    #
    #     if not video_id_match_name:
    #         rstr_video_id = cls.rstr_video_id()
    #     else:
    #         rstr_video_id = RegexTool.name_rstr2named(video_id_match_name, cls.rstr_video_id())
    #     rstr = RegexTool.join("", [rstr_prefix, rstr_video_id])
    #
    #     logger.debug({"rstr": rstr})
    #     return rstr

    # @classmethod
    # def pattern_url(cls, video_id_match_name=None):
    #     rstr = cls.rstr_url(video_id_match_name=video_id_match_name)
    #     return re.compile(rstr)

    @classmethod
    def _url2match_video_id(cls, url):
        m_prefix = cls.pattern_url_prefix().match(url)
        if not m_prefix:
            return None

        m_video_id = cls.pattern_video_id().match(url[m_prefix.end():])
        if not m_video_id:
            return None

        return m_video_id

    @classmethod
    def url2video_id(cls, url):
        m_video_id = cls._url2match_video_id(url)
        if not m_video_id:
            return None

        return m_video_id.group()

    @classmethod
    def video_id2thumbnail_url_hqdefault(cls, video_id):
        return "https://img.youtube.com/vi/{}/hqdefault.jpg".format(video_id)
