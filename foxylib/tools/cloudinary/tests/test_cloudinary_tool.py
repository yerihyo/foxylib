import json
import logging
import os
from pprint import pprint
from unittest import TestCase

import cloudinary.uploader

from foxylib.tools.cloudinary.cloudinary_tool import FoxylibCloudinary, CloudinaryTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestCloudinaryTool(TestCase):
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        # https://cloudinary.com/documentation/upload_images

        filepath = os.path.join(FILE_DIR, "image", "foxytrixy-280x280.png")
        logger.debug({"filepath":filepath})

        with CloudinaryTool.config2activated(FoxylibCloudinary.config()):
            result = cloudinary.uploader.upload(filepath, overwrite=False)

        logger.debug(json.dumps({"result":result}, indent=2))

        self.assertEqual(result["original_filename"], 'foxytrixy-280x280')
        self.assertEqual(result["height"], 280)
        self.assertEqual(result["width"], 280)
        self.assertEqual(result["resource_type"], "image")
        self.assertIn("url", result)
        self.assertIn("secure_url", result)
        self.assertIn("public_id", result)


        sample = {'asset_id': '0db034c9954976a13b2fe1175202b0c1',
               'bytes': 81477,
               'created_at': '2020-07-30T18:50:27Z',
               'etag': '*******************',
               'format': 'png',
               'height': 280,
               'original_filename': 'foxytrixy-280x280',
               'placeholder': False,
               'public_id': 'uuloiltef5jdwx7zjkjm',
               'resource_type': 'image',
               'secure_url': 'https://res.cloudinary.com/foxylib/image/upload/v1596135027/uuloiltef5jdwx7zjkjm.png',
               'signature': '*******************',
               'tags': [],
               'type': 'upload',
               'url': 'http://res.cloudinary.com/foxylib/image/upload/v1596135027/uuloiltef5jdwx7zjkjm.png',
               'version': 1596135027,
               'version_id': 'c1e5a09467e1e7fea61cabc806a7d3cf',
               'width': 280}
