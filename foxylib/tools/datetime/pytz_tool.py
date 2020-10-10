class PytzTool:
    @classmethod
    def localize(cls, dt, tzinfo):
        if tzinfo is None:
            return dt.replace(tzinfo=None)

        return tzinfo.localize(dt)
