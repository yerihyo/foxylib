import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.collections.collections_tool import smap
from future.utils import lmap

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.module.module_tool import ModuleTool


class TestModuleTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        hyp = ModuleTool.x2module(self.__class__)
        ref = "foxylib.tools.native.module.tests.test_module_tool"

        self.assertEqual(hyp, ref)

    def test_02(self):
        cls = self.__class__
        hyp = ModuleTool.class2filepath(cls)
        ref = "/foxylib/tools/native/module/tests/test_module_tool.py"

        self.assertTrue(hyp.endswith(ref))

    def test_03(self):
        hyp = ModuleTool.func2filepath(self.test_03)
        ref = "/foxylib/tools/native/module/tests/test_module_tool.py"

        self.assertTrue(hyp.endswith(ref))

    def test_04(self):
        hyp = ModuleTool.x2filepath(self)
        ref = "/foxylib/tools/native/module/tests/test_module_tool.py"

        self.assertTrue(hyp.endswith(ref))

    def test_05(self):
        from foxylib.tools.native.module.tests.test_module_tool_helper import MODULE
        hyp = smap(str, ModuleTool.module2classes_within(MODULE))
        ref = {"<class 'foxylib.tools.native.module.tests.test_module_tool_helper.A.B'>",
               "<class 'foxylib.tools.native.module.tests.test_module_tool_helper.A.B.C'>",
               "<class 'foxylib.tools.native.module.tests.test_module_tool_helper.A'>"}

        # pprint(hyp)
        self.assertEqual(hyp, ref)
