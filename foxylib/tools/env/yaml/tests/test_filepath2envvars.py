import logging
import os
from functools import reduce
from pathlib import Path
from unittest import TestCase

from jinja2 import UndefinedError

from foxylib.tools.env.lpasslines2envvars import lpasslines_context2envvars
from foxylib.tools.env.yaml.filepaths2envvars import filepaths_context2envvars
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 5, FILE_DIR)


class TestMain(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_1(self):
        filepaths = [
            f"{REPO_DIR}/foxylib/tools/env/yaml/tests/{Path(FILE_PATH).stem}/test_1.sample_1.yaml",
        ]

        h_context = {'ENV': 'dev', 'c':'zzz'}
        envvars = list(filepaths_context2envvars(filepaths, h_context))

        self.assertEqual(envvars, ['A="a2"', 'B="zzz-dev"'])

    def test_2(self):
        filepaths = [
            f"{REPO_DIR}/foxylib/tools/env/yaml/tests/{Path(FILE_PATH).stem}/test_1.sample_1.yaml",
        ]

        h_context = {'ENV': 'dev', }
        with self.assertRaises(UndefinedError):
            list(filepaths_context2envvars(filepaths, h_context))
