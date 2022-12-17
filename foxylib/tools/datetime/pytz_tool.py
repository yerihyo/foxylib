from datetime import datetime


class PytzTool:
    @classmethod
    def localize(cls, dt, tzinfo) -> datetime:
        if tzinfo is None:
            return dt.replace(tzinfo=None)

        return tzinfo.localize(dt)
