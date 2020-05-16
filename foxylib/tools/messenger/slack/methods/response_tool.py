class SlackResponseTool:
    @classmethod
    def response2is_ok(cls, response):
        return response["ok"] is True

    @classmethod
    def response2j_resopnse(cls, response):
        return response.data
