from mimetypes import guess_type




class MimetypeTool:
    class Value:
        TEXT_XPYTHON = "text/x-python"
        TEXT_PLAIN = "text/plain"

        APPLICATION_XHWP = "application/x-hwp"
        APPLICATION_MS_EXCEL = "application/vnd.ms-excel"

    V = Value

    @classmethod
    def url2mimetype(cls, url):
        mimetype, encoding = guess_type(url)
        return mimetype



    @classmethod
    def mimetype2is_ms_excel(cls, mimetype):
        h = {"application/vnd.ms-excel",
             "application/msexcel",
             "application/x-msexcel",
             "application/x-ms-excel",
             "application/x-excel",
             "application/x-dos_ms_excel",
             "application/xls",
             "application/x-xls",
             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
             }
        return mimetype in h
