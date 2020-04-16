import logging
from pprint import pprint
from unittest import TestCase

from foxylib.tools.googleapi.docs.googledocs_tool import GoogledocsTool
from foxylib.tools.googleapi.foxylib_google_api import FoxylibGoogleapi
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class TestGoogledocsTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)

        cred = FoxylibGoogleapi.ServiceAccount.credentials()
        doc = GoogledocsTool.cred_id2document(cred, "12UrF3qdQtKNFdKaGS5UnJxBJzfIXgljzOXO_J73vmXo",)
        hyp = GoogledocsTool.document2text(doc)
        ref = """Testing 
Doc
now

"""

        # pprint(hyp)
        self.assertEquals(hyp, ref)
