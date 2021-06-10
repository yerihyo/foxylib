import logging
import os
from functools import reduce
from pathlib import Path
from pprint import pprint
from unittest import TestCase

from jinja2 import UndefinedError

from foxylib.tools.env.yaml.yaml_env_tool import YamlEnvFile, Lpassline
from foxylib.tools.log.foxylib_logger import FoxylibLogger


FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*5, FILE_DIR)


class TestYamlEnvFile(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        filepath = os.path.join(FILE_DIR, Path(FILE_PATH).stem, "test_1.sample.yaml")
        h_context = {"ENV": "local", 'c':'zzz'}
        kv_list = YamlEnvFile.filepath_context2kv_list(filepath, h_context)

        pprint({'kv_list': kv_list})
        self.assertEqual(kv_list, [('A', 'a1-local'), ('B', 'b1')])

    def test_2(self):
        filepath = os.path.join(FILE_DIR, Path(FILE_PATH).stem, "test_1.sample.yaml")
        h_context = {"ENV": "staging", 'c':'zzz'}
        kv_list = YamlEnvFile.filepath_context2kv_list(filepath, h_context)

        pprint({'kv_list': kv_list})
        self.assertEqual(kv_list, [('B', 'b3')])

    def test_3(self):
        filepath = os.path.join(FILE_DIR, Path(FILE_PATH).stem, "test_1.sample.yaml")
        h_context = {"ENV": "dev",}
        with self.assertRaises(UndefinedError):
            YamlEnvFile.filepath_context2kv_list(filepath, h_context)


class TestLpassline(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        filepath = Lpassline.lpassline_context2filepath(
            " # 12341324 {{REPO_DIR}}/foxylib/tools/env/tests/test_yaml_env_tool/test_1.sample_2.yaml",
            {})
        self.assertEqual(filepath, None)
