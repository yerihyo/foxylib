import logging
import os
from functools import reduce
from unittest import TestCase

from foxylib.tools.env.yaml.yaml_env_tool import Yaml2EnvTool

from foxylib.tools.env.lpasslines2envvars import lpasslines_context2envvars
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 4, FILE_DIR)


class TestMain(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        lpasslines = [
            "12341324 {{REPO_DIR}}/foxylib/tools/env/tests/test_1.sample_1.yaml",
            " # 12341324 {{REPO_DIR}}/foxylib/tools/env/tests/test_1.sample_2.yaml", # comment
            ""
        ]

        h_context = {'REPO_DIR': REPO_DIR, 'ENV': 'dev'}
        envvars = list(lpasslines_context2envvars(lpasslines, h_context, Yaml2EnvTool.value2doublequoted))

        self.assertEqual(envvars, ['A="a2"', 'B="b2-dev"'])