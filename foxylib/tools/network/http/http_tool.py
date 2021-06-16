class HttpTool:
    @classmethod
    def code2is_success(cls, code):
        return code//100 == 2
