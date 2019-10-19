import re
import urllib.parse

from foxylib.tools.collections.collections_tools import merge_dicts, vwrite_overwrite, l_singleton2obj
from foxylib.tools.log.logger_tools import FoxylibLogger


class URLToolkit:
    @classmethod
    def url2utf8_safe(cls, url):
        url_utf8 = re.sub(" ", "+", urllib.parse.unquote(url))
        return url_utf8


    @classmethod
    def append_query2url(cls, url, h_query_in=None):
        logger = FoxylibLogger.func2logger(cls.append_query2url)

        if not h_query_in:
            return url

        url_parts = list(urllib.parse.urlparse(url))
        h_query_ori = dict(urllib.parse.parse_qsl(url_parts[4]))
        h_query = merge_dicts([h_query_ori, h_query_in,], vwrite=vwrite_overwrite)
        # logger.debug({"h_query":h_query, "h_query_ori":h_query_ori, "url_parts":url_parts,})

        url_parts[4] = urllib.parse.urlencode(h_query)

        url_paramed = urllib.parse.urlunparse(url_parts)
        url_utf8 = cls.url2utf8_safe(url_paramed)
        return url_utf8

    @classmethod
    def append_section2url(cls, url, str_section=None,):
        if not str_section:
            return url

        url_all = "#".join([url, str_section])
        return url_all

    @classmethod
    def url2h_query(cls, url):
        p = urllib.parse.urlparse(url)
        h = urllib.parse.parse_qs(p.query)
        return h

    @classmethod
    def url_param2value(cls, url, param):
        h = cls.url2h_query(url)
        l = h.get(param)
        if not l:
            return None

        return l_singleton2obj(l)

    @classmethod
    def rstr(cls):
        return r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'

append_query2url = URLToolkit.append_query2url