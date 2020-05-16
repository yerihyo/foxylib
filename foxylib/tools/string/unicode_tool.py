class UnicodeTool:
    @classmethod
    def utf82surrogate_escaped(cls, utf8):
        # https://github.com/elastic/elasticsearch-py/issues/611
        return utf8.encode('utf-8', "backslashreplace").decode('utf-8')

    @classmethod
    def lstrip_bom(cls, text):
        return text.lstrip('\ufeff')
