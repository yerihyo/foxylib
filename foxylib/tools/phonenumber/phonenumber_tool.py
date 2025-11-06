import re
from functools import lru_cache
from re import Match
from phonenumbers import PhoneNumberFormat, NumberParseException, parse, format_number, is_valid_number

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
    def number_countrycode2e164_DEPRECATED(cls, phonenumber_in:str, countrycode_in:str) -> str:
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

    @classmethod
    def number_iso31662e164(cls, phone_number: str, iso3166alpha2: str) -> str:
        """
        한국 전화번호 문자열을 E.164 형식 (+821012345678)으로 변환합니다.

        :param phone_number: 한국식 전화번호 문자열 (예: '010-1234-5678', '02 123 4567')
        :return: E.164 형식의 문자열, 변환 실패 시 None 반환
        """
        # 1. 예외 처리: 입력된 문자열이 전화번호 형식인지 확인
        try:
            # phonenumbers.parse(번호, 지역 코드)
            # 지역 코드를 'KR'로 지정하여 국내 번호임을 알려줍니다.
            parsed_number = parse(phone_number, iso3166alpha2)
        except NumberParseException:
            # 파싱에 실패하면 None 반환
            return None

        # 2. 유효성 검사 (선택 사항이지만 권장)
        # 번호가 실제 유효한 번호인지 확인합니다.
        if not is_valid_number(parsed_number):
            return None

        # 3. E.164 형식으로 포맷팅
        e164_format = format_number(
            parsed_number,
            PhoneNumberFormat.E164
        )

        return e164_format


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