class PCRETool:
    @classmethod
    def wrapped(cls, regex):
        return f'(?:{regex})'

    @classmethod
    def regexes2joined(cls, regexes, delim):
        return delim.join(map(cls.wrapped, regexes))

    @classmethod
    def regexes2or(cls, regexes):
        return cls.regexes2joined(regexes, "|")

    @classmethod
    def regexes2and(cls, regexes):
        return cls.regexes2joined(regexes, "&")

    @classmethod
    def regex_username(cls):
        return '[-_a-zA-Z0-9.+!%]*'
