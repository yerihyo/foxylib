import logging

from nose.tools import assert_true

from foxylib.tools.collections.collections_tools import l_singleton2obj
from foxylib.tools.json.json_tools import jdown
from foxylib.tools.log.logger_tools import FoxylibLogger


class GoogleOCRTool:
    @classmethod
    def j_page2text(cls, j_page):
        logger = FoxylibLogger.func_level2logger(cls.j_page2text, logging.DEBUG)
        j_response_list = jdown(j_page, ["responses"])
        if j_response_list is None:
            return None

        assert_true(j_response_list, j_page)

        j_response = l_singleton2obj(j_response_list)

        str_text = jdown(j_response, ["fullTextAnnotation", "text"])
        return str_text