import logging
from pprint import pprint
from unittest import TestCase

import pytest

from foxylib.tools.googleapi.docs.googledocs_tool import GoogledocsTool
from foxylib.tools.googleapi.foxylib_googleapi import FoxylibGoogleapi
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestGoogledocsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    @pytest.mark.skip(reason="FileNotFoundError: [Errno 2] No such file or directory: '/Users/moonyoungkang/project/foxylib/foxylib/env/googleapi/foxylib-ff3a87675bbe.json'")
    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        service = GoogledocsTool.credentials2service(cred)
        doc = GoogledocsTool.doc_id2document(service, "12UrF3qdQtKNFdKaGS5UnJxBJzfIXgljzOXO_J73vmXo",)
        hyp = GoogledocsTool.document2text(doc)
        ref = """Testing 
Doc
now

"""

        # pprint(hyp)
        self.assertEquals(hyp, ref)
