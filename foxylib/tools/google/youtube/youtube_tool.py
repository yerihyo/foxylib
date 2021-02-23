import logging
import random
import re
import string
from functools import lru_cache

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool
from foxylib.tools.url.url_tool import URLTool


class YoutubeTool:
    @classmethod
    def str2video_id(cls, str_in):
        m_url = RegexTool.pattern_str2match_full(cls.pattern_url(), str_in)
        if m_url:
            return cls.urlmatch2video_id(m_url)

        m_video_id = RegexTool.pattern_str2match_full(cls.pattern_video_id(), str_in)
        if m_video_id:
            return m_video_id.group()

        return None

    @classmethod
    def video_id2url(cls, video_id):
        url_base = "https://www.youtube.com/watch"
        h = {"v":video_id}
        url = URLTool.append_query2url(url_base, h)
        return url

    @classmethod
    def video_id2thumbnail_url_hqdefault(cls, video_id):
        return "https://img.youtube.com/vi/{}/hqdefault.jpg".format(video_id)

    @classmethod
    def author_channel_id_random(cls,):
        length = 24

        vocab = string.ascii_letters + string.digits
        return ''.join(random.choices(vocab, k=length))

    @classmethod
    def video_id2live_chat_id(cls, credentials, video_id):
        logger = FoxylibLogger.func_level2logger(
            cls.video_id2live_chat_id, logging.DEBUG)

        from foxylib.tools.googleapi.youtube.data.dataapi_tool import \
            DataapiTool, LiveStreamingData

        data = DataapiTool.video_id2live_streaming_data(video_id, credentials)
        live_chat_id = LiveStreamingData.data2chat_id(data)

        logger.debug({"video_id": video_id, 'live_chat_id': live_chat_id})
        return live_chat_id

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_video_id(cls):
        rstr = r"[A-Za-z0-9\-=_]{11}"
        return re.compile(rstr)

    @classmethod
    @lru_cache(maxsize=2)
    def pattern_url(cls):
        # reference: https://stackoverflow.com/a/8260383

        head = RegexTool.rstr2wrapped(r'.*')
        prefix = RegexTool.rstrs2or([
            'watch\?v=',
            r'\/u\/\w\/',
            r'\/v\/',
            r'embed\/',
            r'youtu.be\/',
            r'/video/',
        ])
        rstr_video_id = cls.pattern_video_id().pattern
        # rstr = fr'{head}{prefix}(?P<video_id>[^#&?]*).*'
        rstr = fr'{head}{prefix}(?P<video_id>{rstr_video_id}).*'
        p = re.compile(rstr, re.I)
        return p

    @classmethod
    def url2video_id(cls, url):
        p = cls.pattern_url()

        m = RegexTool.pattern_str2match_full(p, url)
        if not m:
            return None

        return cls.urlmatch2video_id(m)

    @classmethod
    def urlmatch2video_id(cls, match):
        return match.group("video_id")





class Deprecated:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_video_id(cls):
        rstr = r"[A-Za-z0-9\-=_]{11}"
        return re.compile(rstr)

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_url_prefix(cls):
        rstr = r'(?:https?://)?(?:www\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)/(?:watch\?v=|embed/|v/|.+\?v=)?'
        return re.compile(rstr)

    @classmethod
    # @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_url(cls, ):
        logger = FoxylibLogger.func_level2logger(cls.pattern_url, logging.DEBUG)

        rstr_prefix = cls.pattern_url_prefix().pattern
        rstr_video_id = cls.pattern_video_id().pattern
        rstr = RegexTool.join("", [rstr_prefix, rstr_video_id])

        logger.debug({"rstr": rstr})
        return re.compile(rstr)

    @classmethod
    def url2video_id(cls, url):
        def url2match_video_id(url_):
            m_prefix = cls.pattern_url_prefix().match(url_)
            if not m_prefix:
                return None

            match = cls.pattern_video_id().match(url_[m_prefix.end():])
            if not match:
                return None

            return match

        m_video_id = url2match_video_id(url)
        if not m_video_id:
            return None

        return m_video_id.group()
