class StreamToolkit:
    @classmethod
    def stdin2line_list(cls, stdin):
        l = []
        for s in stdin:
            l.append(s)
        return l