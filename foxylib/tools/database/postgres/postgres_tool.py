class PostgresTool:
    @classmethod
    def fetch_iter(cls, cursor):
        while True:
            x = cursor.fetchone()
            if x is None: break
            yield x