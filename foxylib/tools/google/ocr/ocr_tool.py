import logging

from nose.tools import assert_true

from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class GoogleOCRTool:
    @classmethod
    def j_page2text(cls, j_page):
        logger = FoxylibLogger.func_level2logger(cls.j_page2text, logging.DEBUG)
        j_responspan_list = JsonTool.down(j_page, ["responses"])
        if j_responspan_list is None:
            return None

        assert_true(j_responspan_list, j_page)

        j_response = l_singleton2obj(j_responspan_list)

        str_text = JsonTool.down(j_response, ["fullTextAnnotation", "text"])
        return str_text