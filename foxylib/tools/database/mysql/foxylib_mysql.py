import contextlib
import logging
from functools import lru_cache

from MySQLdb.cursors import SSDictCursor

from foxylib.tools.database.mysql.mysql_tool import MysqlTool
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import format_str


class FoxylibMysql:
    @classmethod
    @lru_cache(maxsize=2)
    def conn(cls, *_, **__):
        logger = FoxylibLogger.func_level2logger(cls.conn, logging.DEBUG)

        url = EnvTool.key2value('MYSQL_URL')
        logger.debug({"url":url})

        kwargs_default = {"cursorclass":SSDictCursor}  # Cursor, DictCursor
        kwargs = {**kwargs_default, **__}

        return MysqlTool.url2conn(url, *_, **kwargs)

    @classmethod
    @contextlib.contextmanager
    def cursor_contexted(cls):
        with MysqlTool.conn2cursor_contexted(cls.conn()) as cursor:
            yield cursor


class SampleTable:
    NAME = "sample"

    @classmethod
    @contextlib.contextmanager
    def values2cursor(cls, values):  # value = ['a','b','c','d','e']
        logger = FoxylibLogger.func_level2logger(cls.values2cursor, logging.DEBUG)

        sql = format_str("SELECT * FROM {} WHERE field_name in {}",
                         cls.NAME, "({})".format(", ".join(map("'{}'".format, values)))
                         )
        logger.debug({"sql": sql})

        # with MysqlTool.conn2cursor_contexted(CommonutilsMysql.conn()) as c:
        with FoxylibMysql.cursor_contexted() as c:
            yield MysqlTool.sql2executed(c, sql)

            # for row in c: pass

