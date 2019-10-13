class KhalaResponse:
    class Field:
        TEXT = "text"
    F = Field

    class Builder:
        @classmethod
        def str2j_response(cls, str_out):
            return {KhalaResponse.F.TEXT: str_out}

    @classmethod
    def j_response2text(cls, j_response):
        return j_response[cls.F.TEXT]