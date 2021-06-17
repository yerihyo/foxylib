class HttpTool:
    @classmethod
    def code2is_ok(cls, code):
        return code//100 == 2
