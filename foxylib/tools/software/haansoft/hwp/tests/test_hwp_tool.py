import logging
import os
from tempfile import NamedTemporaryFile
from unittest import TestCase

import pytest

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.software.haansoft.hwp.hwp_tool import HWPTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestHWPTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @classmethod
    def ref(cls):
        return '\n\n<표>\n\n\n\n<표>\n\n\n※ 다가구 등 매입임대란 ?\n한국토지주택공사 등이 도심 내 저소득 계층이 현 생활권에서 안정적으로 거주할 수 있도록 다가구 등 기존주택을 매입하여 개보수 후 시중시세의 30% 수준의 임대조건으로 저렴하게 임대하는 제도입니다.\n\n\n<표>\n\n\n ■ 대상주택 \n  • 서울시 한강이북권역 소재 다가구 주택 51호 (주택소재지, 면적 등은 첨부 “주택내역” 참조)\n    금회 입주자모집 대상주택은 공고일(2018.05.04) 현재 미임대 주택임\n\n  • 주택유형 : 1형(1인 이하 가구용), 2형(2~4인 가구용)\n  • 금회 공급주택의 선순위 접수마감시 후순위 접수는 받지 않음.\n\n  • 공급 과정에서 하자 등 발견시 신청접수 이전에 공급대상주택에서 제외 될 수 있습니다.\n\n  • 가구원수에 따른 주택유형에 대해 1세대 1주택 신청을 원칙으로 하며, 중복 신청하는 경우 전부 무효처리 합니다.\n* 입주대상자가 희망할 경우 작은 규모의 주택에 한하여 신청가능\n* 가구원수는 입주자모집공고일(2018.05.04) 현재 무주택세대구성원 전원을 포함\n\n\n<표>\n\n\n\n<표>\n\n* 2015년 하반기 이후 매입임대주택 관리업무(공용부분 청소, 공과금 배분 등) 외부 위탁이 시행되어 이에 따라 별도의 청소용역비 및 관리비를 부담하셔야 합니다.\n'

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)
        cls = self.__class__

        filepath_hwp = os.path.join(FILE_DIR, "hwp샘플.hwp")
        hyp = HWPTool.filepath2text(filepath_hwp)
        self.assertEqual(hyp, cls.ref())

    @pytest.mark.skip(reason="not necessary because 'HWPTool.filepath2text' works")
    def test_02(self):
        cls = self.__class__

        filepath_hwp = os.path.join(FILE_DIR, "hwp샘플.hwp")
        filepath_text = "/tmp/t.txt"
        HWPTool.filepath2textfile(filepath_hwp, filepath_text)

        hyp = FileTool.filepath2utf8(filepath_text)
        self.assertEqual(hyp, cls.ref())


    def test_03(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)
        cls = self.__class__

        filepath_hwp = os.path.join(FILE_DIR, "hwp샘플.hwp")
        bytes = FileTool.filepath2bytes(filepath_hwp)

        with NamedTemporaryFile() as f:
            f.write(bytes)
            hyp = HWPTool.filepath2text(f.name,)

        logger.debug({"hyp":hyp})
        self.assertEqual(hyp, cls.ref())


