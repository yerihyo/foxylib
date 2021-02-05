import os
import re
import urllib.parse
from functools import lru_cache

import requests

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_overwrite, l_singleton2obj
from foxylib.tools.function.function_tool import FunctionTool


class URLToolConfig:
    class Field:
        SCHEME = "scheme"
        HOST = "host"
        PATH = "path"
        PARAMETERS = "parameters"




class URLTool:
    Config = URLToolConfig

    # @classmethod
    # def j_config2url(cls, j_config):
    #     scheme_raw = j_config[cls.Config.Field.SCHEME]
    #     scheme = "{}://".format(scheme_raw) if scheme_raw and scheme_raw.endswith("://") else scheme_raw
    #
    #     h_params = j_config.get(cls.Config.Field.PARAMETERS)
    #     str_params = "?{}".format(urllib.parse.urlencode(h_params)) if h_params else None
    #
    #     l = [scheme,
    #          j_config.get(cls.Config.Field.HOST),
    #          j_config.get(cls.Config.Field.PATH),
    #          str_params,
    #          ]
    #     return "".join(l)


    @classmethod
    def url2utf8_safe(cls, url):
        url_utf8 = re.sub(" ", "+", urllib.parse.unquote(url))
        return url_utf8


    @classmethod
    def append_query2url(cls, url, h_query_in=None):
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

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern(cls):
        return re.compile(cls.rstr())

    @classmethod
    def url2is_accessible(cls, url):
        httpr = requests.head(url)
        return httpr.ok

    @classmethod
    def url2schemed_auth(cls, url):
        # https://stackoverflow.com/a/41919945

        # scheme://netloc/path;parameters?query#fragment

        o = urllib.parse.urlparse(url)
        return f'{o.scheme}://{o.netloc}'

    @classmethod
    def auth_path2url(cls, auth, path):
        return '/'.join([auth.rstrip('/'), path.lstrip('/')])


class UrlpathTool:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_redundant_prefix(cls):
        return re.compile(r"^[.]")

    @classmethod
    def filepath_pair2url(cls, filepath_target, filepath_root):
        p = cls.pattern_redundant_prefix()
        if not filepath_target.startswith(filepath_root):
            return None

        relpath_raw = os.path.relpath(filepath_target, filepath_root)
        out_1 = p.sub("", relpath_raw)

        out_2 = out_1 if out_1.startswith("/") else "/{}".format(out_1)
        out_3 = out_2 if out_2.endswith("/") else "{}/".format(out_2)
        return out_3


    # @classmethod
    # def class2dirpath(cls, clazz):
    #     str_filepath = ModuleTool.get_module(clazz)
    #     return str_filepath.rsplit(".", 1)[0]
    #
    # @classmethod
    # def class_rootpath2url(cls, clazz, relpath_root):
    #     # str_source = dirpath_root
    #     str_target = cls.class2dirpath(clazz)
    #
    #     k = len(relpath_root)
    #     assert_equal(str_target[:k], relpath_root, )
    #
    #     str_url = str_target[k:].replace(".", "/")
    #     return str_url + "/"
    #
    # @classmethod
    # def class2json_url(cls, clazz):
    #     str_source = cls.class2dirpath(cls)
    #     str_target = cls.class2dirpath(clazz)
    #
    #     k = len(str_source)
    #     assert_equal(str_target[:k], str_source, )
    #
    #     str_url = str_target[k:].replace(".", "/")
    #     return str_url + ".json/"

append_query2url = URLTool.append_query2url