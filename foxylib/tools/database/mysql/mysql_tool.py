import contextlib
import logging
from functools import lru_cache
from urllib.parse import urlparse

import MySQLdb
from MySQLdb.cursors import Cursor, DictCursor

from foxylib.tools.env.env_tool import EnvTool

LOGGER = logging.getLogger(__name__)


class MysqlTool:
    # https://stackoverflow.com/a/8074341
    @classmethod
    def url2conn(cls, url, cursorclass=None):
        if cursorclass is None:
            cursorclass = DictCursor

        p = urlparse(url)

        conn = MySQLdb.connect(
            host=p.hostname,
            user=p.username,
            passwd=p.password,
            db=p.path[1:],
            port=p.port,
            cursorclass=cursorclass,
        )

        return conn

    @classmethod
    @contextlib.contextmanager
    def conn2contexted(cls, conn):
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()

    @classmethod
    @contextlib.contextmanager
    def cursor2contexted(cls, cursor):
        try:
            yield cursor
        finally:
            if cursor:
                cursor.close()

    @classmethod
    @contextlib.contextmanager
    def conn2cursor_contexted(cls, conn_in):
        with cls.conn2contexted(conn_in) as conn:
            with cls.cursor2contexted(conn.cursor()) as cursor:
                yield cursor

    @classmethod
    def sql2executed(cls, cursor, sql):
        cursor.execute(sql)
        return cursor

