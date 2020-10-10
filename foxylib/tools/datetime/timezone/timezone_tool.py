class TimezoneTool:
    @classmethod
    def tzdb2abbreviation(cls, tzdb):
        if tzdb == "Asia/Seoul":
            return "KST"

        if tzdb == "America/Los_Angeles":
            return "ET"

        raise NotImplementedError({"tzdb":tzdb})
