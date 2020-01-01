from mimetypes import guess_type


class MimetypeTool:
    class Value:
        TEXT_XPYTHON = "text/x-python"
        TEXT_PLAIN = "text/plain"
    V = Value

    @classmethod
    def url2mimetype(cls, url):
        mimetype, encoding = guess_type(url)
        return mimetype


