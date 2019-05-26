import re
import urllib.parse

from foxylib.tools.collections.collections_tools import merge_dicts, vwrite_overwrite
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
        logger.debug({"h_query":h_query, "h_query_ori":h_query_ori, "url_parts":url_parts,})

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
