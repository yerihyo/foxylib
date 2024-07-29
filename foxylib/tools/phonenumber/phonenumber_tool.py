import re
from functools import lru_cache
from re import Match


class PhonenumberTool:
    @classmethod
    def x2nodash(cls, x:str) -> str:
        return x.replace('-','')

    @classmethod
    @lru_cache(maxsize=1)
    def pattern_countrycode(cls):
        return re.compile(r'^(?:\+|00)(?:1|7|2[07]|3[0123469]|4[013456789]|5[12345678]|6[0123456]|8[1246]|9[0123458]|(?:2[12345689]|3[578]|42|5[09]|6[789]|8[035789]|9[679]))')

    # @classmethod
    # def countrycode2norm(cls, countrycode):
    #     return countrycode if countrycode[0] == '+' else f'+{countrycode}'

    @classmethod
    def dom2nzdom(cls, countrycode):
        return countrycode if countrycode[0] == '+' else f'+{countrycode}'

    @classmethod
    def number_countrycode2e164(cls, phonenumber_in:str, countrycode_in:str) -> str:
        if not phonenumber_in:
            return None

        phonenumber_nodash = cls.x2nodash(phonenumber_in)

        m:Match[str] = cls.pattern_countrycode().match(phonenumber_nodash)

        dom = phonenumber_nodash[m.end():] if m else phonenumber_nodash
        return ''.join([
            # m.group() if m else (countrycode_in if countrycode_in[0] == '+' else f'+{countrycode_in}'),
            m.group() if m else countrycode_in,
            PhonenumberkrTool.dom2nzdom(dom)
        ])


class PhonenumberkrTool:
    @classmethod
    def is_zdom(cls, dom:str)->bool:
        return dom.startswith('0') if dom else None

    @classmethod
    def dom2zdom(cls, dom:str)->str:
        if not dom:
            return None

        return dom if cls.is_zdom(dom) else f'0{dom}'

    @classmethod
    def dom2nzdom(cls, dom: str) -> str:
        if not dom:
            return None

        return dom[1:] if cls.is_zdom(dom) else dom