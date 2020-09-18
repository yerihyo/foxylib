from urllib.parse import urlparse

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.sql import SQL, Identifier, Literal


class PostgresTool:
    @classmethod
    def url2conn(cls, url):
        p = urlparse(url)

        kwargs = {"host": p.hostname,
                  "user": p.username,
                  "password": p.password,
                  "database": p.path[1:],
                  "port": p.port,
                  }
        conn = psycopg2.connect(**kwargs)
        return conn

    @classmethod
    def fetch_iter(cls, cursor):
        while True:
            x = cursor.fetchone()  # psycopg2 is smart. paging on its own
            if x is None:
                break
            yield x

    @classmethod
    def format_sql(cls, sql, *_, **__):
        return sql.format(*_, **__)

    @classmethod
    def join(cls, delim, item_list):
        if not item_list:
            return None

        if len(item_list) == 1:
            return item_list[0]

        return delim.join(item_list)

    @classmethod
    def conn2dict_cursor(cls, conn):
        return conn.cursor(cursor_factory=DictCursor)

    @classmethod
    def sql2rows(cls, conn, sql, conn2cursor=None):
        if conn2cursor is None:
            conn2cursor = lambda conn: conn.cursor()

        with conn:
            with conn2cursor(conn) as cursor:
                cursor.execute(sql)
                yield from PostgresTool.fetch_iter(cursor)

    @classmethod
    def fieldname2sql_is_not_null(cls, fieldname, ):
        return SQL("{} IS NOT NULL").format(Identifier(fieldname), )

    @classmethod
    def values2sql_in(cls, fieldname, values):
        return SQL("{} IN {}").format(Identifier(fieldname), Literal(tuple(values)))

    @classmethod
    def values2sql_not_in(cls, fieldname, values):
        return SQL("{} NOT IN {}").format(Identifier(fieldname), Literal(tuple(values)))

    @classmethod
    def datetime_span2sql(cls, fieldname, datetime_span):
        dt_start, dt_end = datetime_span
        sql_list = [SQL("{} >= {}").format(Identifier(fieldname), Literal(dt_start)),
                    SQL("{} <= {}").format(Identifier(fieldname), Literal(dt_end)),
                    ]
        sql = PostgresTool.join(SQL(" AND "), sql_list)
        return sql
