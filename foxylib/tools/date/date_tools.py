import os
import re, yaml
from functools import lru_cache

from dateutil import relativedelta
from future.utils import lmap

from foxylib.tools.native.builtin_tools import IntToolkit
from foxylib.tools.native.class_tools import ClassToolkit
from foxylib.tools.collections.collections_tools import l_singleton2obj
from foxylib.tools.file.file_tools import FileToolkit
from foxylib.itertools.itertools_tools import lchain
from foxylib.tools.log.logger_tools import LoggerToolkit
from foxylib.tools.string.string_tools import format_str


FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class RelativeDeltaToolkit:

    @classmethod
    @lru_cache(maxsize=2)
    def yaml(cls):
        filepath = os.path.join(FILE_DIR, "{0}.yaml".format(ClassToolkit.cls2name(cls)))
        utf8 = FileToolkit.filepath2utf8(filepath)
        j_yaml = yaml.load(utf8)
        return j_yaml

    @classmethod
    def reldelta_name_list(cls):
        return ["years", "months", "weeks", "days", "hours", "minutes", "seconds",]

    # @classmethod
    # def name_value_list2reldelta(cls, ):
    #     return relativedelta.relativedelta(**{name:value})


    @classmethod
    def pattern_timedelta(cls):
        logger = LoggerToolkit.func2logger(cls.pattern_timedelta)

        j_yaml = cls.yaml()

        reldalta_name_list = cls.reldelta_name_list()

        j_reldelta = j_yaml["relativedelta"]
        j_name2strs = lambda j: lchain.from_iterable(j.values())
        rstr_reldelta_list = [format_str(r"(?:(?P<{0}>\d+)\s*(?:{1}))?",
                                         k,
                                         r"|".join(lmap(re.escape, j_name2strs(j_reldelta[k]))),
                                         )
                     for k in reldalta_name_list]
        rstr_reldeltas = r"\s*".join([r"(?:{0})".format(rstr) for rstr in rstr_reldelta_list])

        rstr = r"\s*".join([r"(?P<sign>[+-])", rstr_reldeltas])
        logger.debug({"rstr":rstr})
        pattern = re.compile(rstr, re.IGNORECASE)
        return pattern

    @classmethod
    def parse_str2reldelta(cls, s):
        logger = LoggerToolkit.func2logger(cls.parse_str2reldelta)

        p = cls.pattern_timedelta()
        m_list = list(p.finditer(s))
        if not m_list: return None

        m = l_singleton2obj(m_list)
        int_sign = IntToolkit.parse_sign2int(m.group("sign"))

        kv_list = [(k, int_sign*int(m.group(k)))
                   for k in cls.reldelta_name_list() if m.group(k)]

        logger.debug({"kv_list":kv_list})
        reldelta = relativedelta.relativedelta(**dict(kv_list))
        return reldelta








